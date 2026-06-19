from sqlalchemy.orm import Session
from app.models.advice_model import Advice


class AdviceService:

    @staticmethod
    def get_all_advice(db: Session):
        """
        Recupera de manera eficiente todos los consejos usando la sesión activa.
        """
        advice_list = db.query(Advice).all()
        return [
            {
                "id": advice.id,
                "title": advice.title,
                "content": advice.content,
            }
            for advice in advice_list
        ]