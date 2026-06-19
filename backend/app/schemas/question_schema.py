from pydantic import BaseModel
from typing import List, Optional, Dict

class QuestionSchema(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = []