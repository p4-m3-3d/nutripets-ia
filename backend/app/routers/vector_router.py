from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Asegúrate de importar tu función para obtener la sesión (normalmente en app.core.database o app.dependencies)
from app.core.database import get_db 
from app.ai.vector_loader import VectorLoader

router = APIRouter(
    prefix="/vector",
    tags=["Vector"]
)

@router.post("/load")
def load_vectors(db: Session = Depends(get_db)):
    """
    Endpoint expuesto en Swagger para recrear e indexar 
    los vectores en ChromaDB usando la sesión activa.
    """
    return VectorLoader.load_all(db=db)