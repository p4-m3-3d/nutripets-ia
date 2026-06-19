from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.toxic_ingredient_service import ToxicIngredientService

router = APIRouter(
    prefix="/toxic-ingredients",
    tags=["Toxic Ingredients"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_toxic_ingredients(db: Session = Depends(get_db)):
    """
    Lista todos los ingredientes nocivos o prohibidos para mascotas.
    """
    return ToxicIngredientService.get_all_toxic_ingredients(db=db)