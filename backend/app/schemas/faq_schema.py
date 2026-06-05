from pydantic import BaseModel

class FAQSchema(BaseModel):
    id: int
    question: str
    answer: str