from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.toxic_ingredient_model import ToxicIngredient


class ToxicIngredientService:

    @staticmethod
    def get_all_toxic_ingredients():

        db: Session = SessionLocal()

        try:

            ingredients = db.query(
                ToxicIngredient
            ).all()

            result = []

            for ingredient in ingredients:

                result.append({
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "danger_level": ingredient.danger_level,
                    "symptoms": ingredient.symptoms,
                    "action_required": ingredient.action_required
                })

            return result

        finally:
            db.close()