from fastapi import FastAPI

from app.routers.recipe_router import (
    router as recipe_router
)

from app.routers.advice_router import (
    router as advice_router
)

from app.routers.faq_router import (
    router as faq_router
)

from app.routers.toxic_ingredient_router import (
    router as toxic_ingredient_router
)
from app.routers.data_loader_router import (
    router as data_loader_router
)

app = FastAPI(
    title="NutriPets IA",
    version="1.0.0"
)

app.include_router(recipe_router)
app.include_router(advice_router)
app.include_router(faq_router)
app.include_router(toxic_ingredient_router)
app.include_router(data_loader_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a NutriPets IA"
    }