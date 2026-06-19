from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recipe_service import RecipeService
from app.schemas.recipe_schema import RecipeSchema

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_recipes(db: Session = Depends(get_db)):
    return RecipeService.get_all_recipes(db=db)


@router.get("/search", status_code=status.HTTP_200_OK)
def search_recipes(name: str = Query(...), db: Session = Depends(get_db)):
    return RecipeService.search_recipes(name=name, db=db)


@router.get("/{recipe_id}", status_code=status.HTTP_200_OK)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return RecipeService.get_recipe_by_id(recipe_id=recipe_id, db=db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_payload: RecipeSchema, db: Session = Depends(get_db)):
    return RecipeService.create_recipe(recipe_data=recipe_payload, db=db)


@router.put("/{recipe_id}", status_code=status.HTTP_200_OK)
def update_recipe(recipe_id: int, recipe_payload: RecipeSchema, db: Session = Depends(get_db)):
    return RecipeService.update_recipe(recipe_id=recipe_id, recipe_data=recipe_payload, db=db)


@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return RecipeService.delete_recipe(recipe_id=recipe_id, db=db)