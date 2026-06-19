from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.ai.toxic_detector import ToxicDetector  
from app.ai.toxic_semantic_detector import ToxicSemanticDetector
from app.ai.query_analyzer import QueryAnalyzer
from app.ai.chroma_client import get_collection
from app.ai.embedding_service import create_embedding
from app.ai.llm_service import LLMService

class RagService:

    @staticmethod
    def ask(question: str, db: Session, history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        
        species_text_map = {1: "Perro", 2: "Gato"}
        stage_text_map = {1: "Cachorro", 2: "Adulto", 3: "Senior"}

        # =========================================================
        # PASO 1: ANÁLISIS INTELIGENTE CON CONTEXTO DE HISTORIAL
        # =========================================================
        extracted_metadata = QueryAnalyzer.analyze_query(question, history)
        species_id = extracted_metadata.get("species_id")
        life_stage_id = extracted_metadata.get("life_stage_id")
        is_emergency_by_llm = extracted_metadata.get("is_emergency", False)

        print(f"[DEBUG RAG] Filtros -> Especie ID: {species_id}, Etapa ID: {life_stage_id}, Emergencia: {is_emergency_by_llm}")

        species_detected_str = species_text_map.get(species_id, "General / Ambos")
        life_stage_detected_str = stage_text_map.get(life_stage_id, "Cualquiera")

        # =========================================================
        # PASO 2: DETECTORES DE TOXICIDAD TRADICIONALES
        # =========================================================
        toxic_result = ToxicDetector.detect(question)
        if toxic_result.get("found"):
            return {
                "question": question, "alert": True,
                "answer": f"⚠️ <strong>¡EMERGENCIA TÓXICA DIRECTA!</strong> Riesgo con: {toxic_result.get('ingredient')}.<br><br><strong>Acción inmediata:</strong> {toxic_result.get('recommended_action') or toxic_result.get('action_required')}<br><br><strong>Síntomas:</strong> {toxic_result.get('symptoms')}",
                "recommendations": [], "sources_found": 0, "detected_species": "Alerta Crítica", "detected_life_stage": "Inmediata"
            }

        semantic_toxic = ToxicSemanticDetector.detect(question, db)
        if semantic_toxic:
            return {
                "question": question, "alert": True,
                "answer": f"⚠️ <strong>¡ALERTA DE RIESGO SEMÁNTICO!</strong> Coincidencia con: {semantic_toxic.get('name')}.<br><br><strong>Peligro:</strong> {semantic_toxic.get('danger_level')}<br><strong>Acción requerica:</strong> {semantic_toxic.get('action_required')}<br><br><strong>Síntomas:</strong> {semantic_toxic.get('symptoms')}",
                "recommendations": [], "sources_found": 0, "detected_species": "Alerta Crítica", "detected_life_stage": "Inmediata"
            }

        if is_emergency_by_llm:
            return {
                "question": question, "alert": True,
                "answer": "⚠️ <strong>¡ALERTA DE SEGURIDAD CRÍTICA!</strong> Has mencionado la ingesta de un ingrediente altamente peligroso. Por la salud de tu mascota, suspendemos la recomendación de recetas caseras de inmediato. <strong>Acude de urgencia a una clínica veterinaria.</strong>",
                "recommendations": [], "sources_found": 0, "detected_species": species_detected_str, "detected_life_stage": life_stage_detected_str
            }

        # =========================================================
        # PASO 3: FILTROS DINÁMICOS DE CHROMADB
        # =========================================================
        chroma_filter = {}
        filters_list = []
        if species_id is not None: filters_list.append({"species_id": species_id})
        if life_stage_id is not None: filters_list.append({"life_stage_id": life_stage_id})

        if len(filters_list) == 1: chroma_filter = filters_list[0]
        elif len(filters_list) > 1: chroma_filter = {"$and": filters_list}
        else: chroma_filter = None

        # =========================================================
        # PASO 4: FLUJO RAG Y FORMATEO ENRIQUECIDO EN RESPUESTA
        # =========================================================
        try:
            query_vector = create_embedding(question)
            collection = get_collection()
            
            search_args = {"query_embeddings": [query_vector], "n_results": 4}
            if chroma_filter: search_args["where"] = chroma_filter

            chroma_results = collection.query(**search_args)
            context_documents = []
            recommendations = []
            
            if chroma_results and chroma_results.get("documents") and len(chroma_results["documents"][0]) > 0:
                for i in range(len(chroma_results["documents"][0])):
                    doc_text = chroma_results["documents"][0][i]
                    meta = chroma_results["metadatas"][0][i] if chroma_results.get("metadatas") else {}
                    context_documents.append(doc_text)
                    
                    if meta.get("type") == "recipe":
                        recommendations.append({
                            "title": meta.get("title", "Receta Sugerida"),
                            "species": species_text_map.get(meta.get("species_id"), "General"),
                            "life_stage": stage_text_map.get(meta.get("life_stage_id"), "Cualquiera"),
                            "category": meta.get("category", "Nutritivo")
                        })

            context_str = "\n\n".join(context_documents)
            
            # Ajustamos el prompt para forzar el uso de etiquetas HTML seguras y organizadas
            prompt_final = f"""
            Eres un experto en nutrición animal de NutriPets. Responde la duda del usuario basándote únicamente en el contexto veterinario adjunto.
            
            Reglas de formato obligatorias:
            - Usa listas ordenadas con <ol class="list-decimal ml-4 space-y-1"> y <li> para pasos.
            - Usa listas de viñetas con <ul class="list-disc ml-4 space-y-1"> y <li> para ingredientes o tips.
            - Usa <strong>texto</strong> para resaltar puntos clave o advertencias.
            - Separa los párrafos usando saltos de línea claros.
            
            Contexto:
            {context_str if context_str else "No hay lineamientos específicos en la base de datos."}
            
            Pregunta: "{question}"
            
            Respuesta estructurada en HTML:
            """
            
            llm_response = LLMService.generate(question=prompt_final, context=context_str)

            return {
                "question": question,
                "alert": False,
                "answer": llm_response,
                "recommendations": recommendations,
                "sources_found": len(context_documents),
                "detected_species": species_detected_str,
                "detected_life_stage": life_stage_detected_str
            }

        except Exception as e:
            import traceback
            print("\n❌ [ERROR CRÍTICO EN RAG_SERVICE DETECTADO] ❌")
            traceback.print_exc()  
            raise e