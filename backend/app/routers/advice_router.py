from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.advice_service import AdviceService

router = APIRouter(
    prefix="/advice",
    tags=["Advice"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_advice(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de consejos nutricionales.
    """
    return AdviceService.get_all_advice(db=db)