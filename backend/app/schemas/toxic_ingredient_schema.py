from pydantic import BaseModel

class ToxicIngredientSchema(BaseModel):
    id: int
    name: str
    danger_level: str
    symptoms: str
    action_required: str