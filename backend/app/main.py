import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.database import Base
from app.core.database import engine

# Importar modelos para que SQLAlchemy los registre
from app.models.recipe_model import Recipe
from app.models.advice_model import Advice
from app.models.faq_model import FAQ
from app.models.toxic_ingredient_model import ToxicIngredient

from app.routers.ai_router import router as ai_router
from app.routers.recipe_router import router as recipe_router
from app.routers.advice_router import router as advice_router
from app.routers.faq_router import router as faq_router
from app.routers.toxic_ingredient_router import router as toxic_ingredient_router
from app.routers.data_loader_router import router as data_loader_router
from app.routers.vector_router import router as vector_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriPets IA",
    version="1.0.0",
    description="API para recomendaciones nutricionales y detección de riesgos para mascotas."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe_router)
app.include_router(advice_router)
app.include_router(faq_router)
app.include_router(toxic_ingredient_router)
app.include_router(data_loader_router)
app.include_router(ai_router)
app.include_router(vector_router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a NutriPets IA",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }