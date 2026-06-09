import ollama


class LLMService:

    @staticmethod
    def generate(context: str, question: str):

        prompt = f"""
Eres NutriPets IA, un asistente especializado en nutrición para mascotas.

Responde únicamente usando la información proporcionada.

Contexto:

{context}

Pregunta:

{question}

Respuesta:
"""

        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]