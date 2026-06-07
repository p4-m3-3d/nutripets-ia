from fastapi import APIRouter

from app.services.toxic_ingredient_service import (
    ToxicIngredientService
)

router = APIRouter(
    prefix="/toxic-ingredients",
    tags=["Toxic Ingredients"]
)


@router.get("/")
def get_toxic_ingredients():
    return (
        ToxicIngredientService
        .get_all_toxic_ingredients()
    )