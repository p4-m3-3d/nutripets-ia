import app.models
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.recipe_model import Recipe


class RecipeService:

    @staticmethod
    def get_all_recipes():

        db: Session = SessionLocal()

        try:

            recipes = db.query(Recipe).all()

            result = []

            for recipe in recipes:

                result.append({
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description,
                    "preparation_time": recipe.preparation_time,
                    "difficulty": recipe.difficulty,
                    "calories": recipe.calories
                })

            return result

        finally:
            db.close()

    @staticmethod
    def get_recipe_by_id(recipe_id: int):

        db: Session = SessionLocal()

        try:

            recipe = db.query(Recipe).filter(
                Recipe.id == recipe_id
            ).first()

            if recipe is None:
                raise HTTPException(
                    status_code=404,
                    detail="Receta no encontrada"
            )

            return {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "preparation_time": recipe.preparation_time,
                "difficulty": recipe.difficulty,
                "calories": recipe.calories
            }

        finally:
            db.close()

    @staticmethod
    def create_recipe(recipe_data):

        db: Session = SessionLocal()

        try:

            new_recipe = Recipe(
                title=recipe_data.title,
                description=recipe_data.description,
                preparation=recipe_data.preparation,
                preparation_time=recipe_data.preparation_time,
                difficulty=recipe_data.difficulty,
                calories=recipe_data.calories,
                species_id=1,
                life_stage_id=1,
                category_id=1
            )

            db.add(new_recipe)
            db.commit()
            db.refresh(new_recipe)

            return {
                "message": "Receta creada correctamente",
                "id": new_recipe.id
            }

        finally:
            db.close()

    @staticmethod
    def update_recipe(recipe_id: int, recipe_data):

        db: Session = SessionLocal()

        try:

            recipe = db.query(Recipe).filter(
                Recipe.id == recipe_id
            ).first()

            if recipe is None:
                raise HTTPException(
                    status_code=404,
                    detail="Receta no encontrada"
                )

            recipe.title = recipe_data.title
            recipe.description = recipe_data.description
            recipe.preparation = recipe_data.preparation
            recipe.preparation_time = recipe_data.preparation_time
            recipe.difficulty = recipe_data.difficulty
            recipe.calories = recipe_data.calories

            db.commit()

            return {
                "message": "Receta actualizada correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def delete_recipe(recipe_id: int):

        db: Session = SessionLocal()

        try:

            recipe = db.query(Recipe).filter(
                Recipe.id == recipe_id
            ).first()

            if recipe is None:
                raise HTTPException(
                    status_code=404,
                    detail="Receta no encontrada"
            )

            db.delete(recipe)
            db.commit()

            return {
                "message": "Receta eliminada correctamente"
            }

        finally:
            db.close()

    @staticmethod
    def search_recipes(name: str):

        db: Session = SessionLocal()

        try:

            recipes = db.query(Recipe).filter(
                Recipe.title.like(f"%{name}%")
            ).all()

            result = []

            for recipe in recipes:

                result.append({
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description,
                    "preparation_time": recipe.preparation_time,
                    "difficulty": recipe.difficulty,
                    "calories": recipe.calories
                })

            return result

        finally:
            db.close()