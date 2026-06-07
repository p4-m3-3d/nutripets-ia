from fastapi import APIRouter
from fastapi import Query

from app.services.recipe_service import RecipeService
from app.schemas.recipe_schema import RecipeSchema

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


@router.get("/")
def get_recipes():
    return RecipeService.get_all_recipes()


@router.get("/search")
def search_recipes(
    name: str = Query(...)
):
    return RecipeService.search_recipes(name)


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    return RecipeService.get_recipe_by_id(recipe_id)


@router.post("/")
def create_recipe(recipe: RecipeSchema):
    return RecipeService.create_recipe(recipe)


@router.put("/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe: RecipeSchema
):
    return RecipeService.update_recipe(
        recipe_id,
        recipe
    )


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int):
    return RecipeService.delete_recipe(recipe_id)