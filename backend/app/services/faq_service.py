from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.faq_model import FAQ


class FAQService:

    @staticmethod
    def get_all_faq():

        db: Session = SessionLocal()

        try:

            faq_list = db.query(FAQ).all()

            result = []

            for faq in faq_list:

                result.append({
                    "id": faq.id,
                    "question": faq.question,
                    "answer": faq.answer
                })

            return result

        finally:
            db.close()