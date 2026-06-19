import ollama

class LLMService:

    @staticmethod
    def generate(context: str, question: str) -> str:
        system_instruction = (
            "Eres NutriPets IA, un asistente experto y especializado en nutrición para mascotas. "
            "Tu deber es responder a las consultas de manera clara, amable y profesional. "
            "IMPORTANTE: Responde ÚNICAMENTE usando la información proporcionada en el contexto. "
            "Si el contexto no contiene la respuesta, di amablemente que no dispones de esa información."
        )

        user_content = f"Contexto:\n{context}\n\nPregunta:\n{question}\n\nRespuesta:"

        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content}
            ]
        )

        return response["message"]["content"]