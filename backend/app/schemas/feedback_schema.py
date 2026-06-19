from pydantic import BaseModel

class FeedbackSchema(BaseModel):
    question: str
    answer: str
    is_like: bool