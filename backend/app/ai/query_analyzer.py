import json
from typing import List, Dict, Optional
from app.ai.llm_service import LLMService

class QueryAnalyzer:

    @staticmethod
    def analyze_query(question: str, history: Optional[List[Dict[str, str]]] = None):
        """
        Usa el LLM para identificar de manera inteligente el sujeto afectado,
        evaluando tanto la pregunta actual como el historial de la conversación.
        """
        # Formatear el historial para el prompt
        history_str = ""
        if history:
            for msg in history[-4:]: # Analizamos los últimos 4 mensajes para no saturar el contexto
                role = "Usuario" if msg.get("role") == "user" else "Asistente"
                history_str += f"{role}: {msg.get('content')}\n"

        prompt = f"""
        Analiza la siguiente conversación y la última consulta del usuario para extraer los metadatos necesarios.
        
        Historial reciente:
        {history_str if history_str else "No hay historial previo."}
        
        Última Consulta: "{question}"
        
        Debes responder ÚNICAMENTE con un objeto JSON plano que contenga las siguientes llaves:
        - "species": Debe ser "perro", "gato" o null (Dedúcelo del historial si en la última pregunta no se menciona).
        - "life_stage": Debe ser "cachorro", "adulto", "senior" o null (Dedúcelo del historial si es necesario).
        - "is_emergency": True si el usuario menciona ingesta de tóxicos o venenos inminentes en su última consulta, de lo contrario false.
        
        Ejemplo de salida: {{"species": "gato", "life_stage": "adulto", "is_emergency": false}}
        """
        
        try:
            response_text = LLMService.generate(
                question=prompt,
                context="Análisis de entidades y contexto histórico para NutriPets."
            ) 
            
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            species_map = {"perro": 1, "gato": 2}
            life_stage_map = {"cachorro": 1, "adulto": 2, "senior": 3}
            
            return {
                "species_id": species_map.get(data.get("species")),
                "life_stage_id": life_stage_map.get(data.get("life_stage")),
                "is_emergency": data.get("is_emergency", False)
            }
        except Exception as e:
            print(f"[ERROR] QueryAnalyzer inteligente: {e}")
            return {"species_id": None, "life_stage_id": None, "is_emergency": False}