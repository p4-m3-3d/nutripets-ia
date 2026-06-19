from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de los routers de la aplicación
from app.routers import ai_router
from app.routers import feedback_router  # Asegúrate de que el archivo se llame feedback_router.py

app = FastAPI(
    title="NutriPets IA",
    description="API de soporte nutricional y detección de riesgos para mascotas",
    version="1.0.0"
)

# =========================================================
# CONFIGURACIÓN DE CORS
# =========================================================
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "*",  # Permite pruebas globales, puedes acotarlo después
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# REGISTRO DE ROUTERS (INYECCIÓN DE RUTAS)
# =========================================================
app.include_router(ai_router.router)
app.include_router(feedback_router.router)  # <-- Registramos de forma definitiva las calificaciones de feedback


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "NutriPets IA Engine",
        "version": "1.0.0"
    }