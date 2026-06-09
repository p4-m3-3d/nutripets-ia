import ollama

response = ollama.chat(
    model="mistral",
    messages=[
        {
            "role": "user",
            "content": "Responde únicamente: NutriPets conectado correctamente"
        }
    ]
)

print(
    response["message"]["content"]
)