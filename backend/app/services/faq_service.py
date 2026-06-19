from sqlalchemy.orm import Session
from app.models.faq_model import FAQ


class FAQService:

    @staticmethod
    def get_all_faq(db: Session):
        """
        Recupera el listado completo de preguntas frecuentes.
        """
        faq_list = db.query(FAQ).all()
        return [
            {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer,
            }
            for faq in faq_list
        ]