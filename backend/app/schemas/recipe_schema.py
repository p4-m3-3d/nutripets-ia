from pydantic import BaseModel
from typing import Optional, Literal

class RecipeSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    preparation: str
    preparation_time: Optional[int] = None
    difficulty: Literal["Fácil", "Media", "Difícil"]
    calories: Optional[int] = None
    
    # Campos relacionales opcionales para evitar errores de validación
    species_id: Optional[int] = 1
    life_stage_id: Optional[int] = 1
    category_id: Optional[int] = 1

    class Config:
        from_attributes = True