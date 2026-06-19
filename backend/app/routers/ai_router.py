from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db 

from app.ai.vector_loader import VectorLoader
from app.ai.search_service import SearchService
from app.ai.rag_service import RagService
from app.schemas.question_schema import QuestionSchema
from app.schemas.search_schema import SearchSchema

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)

@router.post("/index", status_code=status.HTTP_201_CREATED)
def create_index(db: Session = Depends(get_db)):
    try:
        return VectorLoader.load_all(db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al indexar vectores: {str(e)}"
        )

@router.post("/search", status_code=status.HTTP_200_OK)
def semantic_search(search_payload: SearchSchema):
    return SearchService.search(query=search_payload.query)

@router.post("/ask", status_code=status.HTTP_200_OK)
def ask_question(question_payload: QuestionSchema, db: Session = Depends(get_db)):
    try:
        # Se envía la pregunta y la lista del historial al servicio RAG
        return RagService.ask(
            question=question_payload.question, 
            db=db, 
            history=question_payload.history
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en el servicio RAG: {str(e)}"
        )