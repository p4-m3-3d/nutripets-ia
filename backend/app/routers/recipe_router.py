from fastapi import APIRouter
from app.services.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.get("/")
def get_recipes():
    return RecipeService.get_all_recipes()
