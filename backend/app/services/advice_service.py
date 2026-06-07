from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.advice_model import Advice


class AdviceService:

    @staticmethod
    def get_all_advice():

        db: Session = SessionLocal()

        try:

            advice_list = db.query(Advice).all()

            result = []

            for advice in advice_list:

                result.append({
                    "id": advice.id,
                    "title": advice.title,
                    "content": advice.content
                })

            return result

        finally:
            db.close()