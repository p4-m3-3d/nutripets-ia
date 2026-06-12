from app.core.database import SessionLocal
from app.models.toxic_ingredient_model import ToxicIngredient

class ToxicDetector:

    @staticmethod
    def detect(question: str):

        db = SessionLocal()

        try:

            ingredients = db.query(
                ToxicIngredient
            ).all()

            question_lower = question.lower()

            for ingredient in ingredients:

                if ingredient.name.lower() in question_lower:

                    return {
                        "found": True,
                        "ingredient": ingredient.name,
                        "danger_level": ingredient.danger_level,
                        "symptoms": ingredient.symptoms,
                        "action_required": ingredient.action_required
                    }

            return {
                "found": False
            }

        finally:
            db.close()
