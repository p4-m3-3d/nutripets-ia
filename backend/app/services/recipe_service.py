from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.recipe_model import Recipe
from app.schemas.recipe_schema import RecipeSchema


class RecipeService:

    @staticmethod
    def get_all_recipes(db: Session):
        recipes = db.query(Recipe).all()
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "preparation_time": recipe.preparation_time,
                "difficulty": recipe.difficulty,
                "calories": recipe.calories,
            }
            for recipe in recipes
        ]

    @staticmethod
    def get_recipe_by_id(recipe_id: int, db: Session):
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receta no encontrada",
            )

        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "preparation_time": recipe.preparation_time,
            "difficulty": recipe.difficulty,
            "calories": recipe.calories,
        }

    @staticmethod
    def create_recipe(recipe_data: RecipeSchema, db: Session):
        new_recipe = Recipe(
            title=recipe_data.title,
            description=recipe_data.description,
            preparation=recipe_data.preparation,
            preparation_time=recipe_data.preparation_time,
            difficulty=recipe_data.difficulty,
            calories=recipe_data.calories,
            species_id=getattr(recipe_data, "species_id", 1),
            life_stage_id=getattr(recipe_data, "life_stage_id", 1),
            category_id=getattr(recipe_data, "category_id", 1),
        )

        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        return {
            "message": "Receta creada correctamente",
            "id": new_recipe.id,
        }

    @staticmethod
    def update_recipe(recipe_id: int, recipe_data: RecipeSchema, db: Session):
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receta no encontrada",
            )

        recipe.title = recipe_data.title
        recipe.description = recipe_data.description
        recipe.preparation = recipe_data.preparation
        recipe.preparation_time = recipe_data.preparation_time
        recipe.difficulty = recipe_data.difficulty
        recipe.calories = recipe_data.calories

        db.commit()
        return {"message": "Receta actualizada correctamente"}

    @staticmethod
    def delete_recipe(recipe_id: int, db: Session):
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receta no encontrada",
            )

        db.delete(recipe)
        db.commit()
        return {"message": "Receta eliminada correctamente"}

    @staticmethod
    def search_recipes(name: str, db: Session):
        recipes = db.query(Recipe).filter(Recipe.title.like(f"%{name}%")).all()
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "preparation_time": recipe.preparation_time,
                "difficulty": recipe.difficulty,
                "calories": recipe.calories,
            }
            for recipe in recipes
        ]