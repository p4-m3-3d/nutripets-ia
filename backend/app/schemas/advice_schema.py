from pydantic import BaseModel

class AdviceSchema(BaseModel):
    id: int
    title: str
    content: str