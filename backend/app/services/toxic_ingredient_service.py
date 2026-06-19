from sqlalchemy.orm import Session
from app.models.toxic_ingredient_model import ToxicIngredient


class ToxicIngredientService:

    @staticmethod
    def get_all_toxic_ingredients(db: Session):
        """
        Retorna los ingredientes nocivos mapeados para el consumo del frontend.
        """
        ingredients = db.query(ToxicIngredient).all()
        return [
            {
                "id": ingredient.id,
                "name": ingredient.name,
                "danger_level": ingredient.danger_level,
                "symptoms": ingredient.symptoms,
                "action_required": ingredient.action_required,
            }
            for ingredient in ingredients
        ]