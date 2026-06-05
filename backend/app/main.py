from fastapi import FastAPI

from app.routers.recipe_router import router as recipe_router

app = FastAPI(
    title="NutriPets IA",
    version="1.0.0"
)

app.include_router(recipe_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a NutriPets IA"
    }
