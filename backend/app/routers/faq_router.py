from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.faq_service import FAQService

router = APIRouter(
    prefix="/faq",
    tags=["FAQ"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_faq(db: Session = Depends(get_db)):
    """
    Obtiene las preguntas frecuentes de la plataforma.
    """
    return FAQService.get_all_faq(db=db)