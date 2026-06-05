from pydantic import BaseModel

class RecipeSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    preparation: str
    preparation_time: int | None = None
    difficulty: str
    calories: int | None = None
    