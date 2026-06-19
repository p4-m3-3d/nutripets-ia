from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.feedback_model import Feedback
from app.schemas.feedback_schema import FeedbackSchema
from fastapi import APIRouter


router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/rate")
def rate_response(payload: FeedbackSchema, db: Session = Depends(get_db)):
    try:
        new_feedback = Feedback(
            question=payload.question,
            answer=payload.answer,
            is_like=payload.is_like
        )
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return {"status": "success", "message": "¡Gracias por tu retroalimentación!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar feedback: {str(e)}")