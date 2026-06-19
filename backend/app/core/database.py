import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Localización y carga del entorno (.env)
BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_ROOT / ".env")

# 2. Recuperación y validación de variables de entorno
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "nutripets_db")

# Construcción de la URI de conexión (MySQL con PyMySQL)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Creación del motor con políticas de re-conexión automática
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True solo si necesitas depurar SQL en consola
    pool_pre_ping=True,
    pool_recycle=3600  # Recicla conexiones cada hora para evitar caídas por timeout de MySQL
)

# 4. Fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 5. Clase base moderna para mapeo de modelos (SQLAlchemy 2.0 Style)
class Base(DeclarativeBase):
    pass


# 6. Dependencia para inyección en los Routers de FastAPI
def get_db() -> Generator:
    """
    Genera una sesión de base de datos para la petición actual y 
    la cierra de manera segura una vez concluida la operación HTTP.
    """
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()