from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), nullable=False)
    answer = Column(String(2000), nullable=False)
    is_like = Column(Boolean, nullable=False)  # True = Like, False = Dislike
    created_at = Column(DateTime, default=datetime.utcnow)