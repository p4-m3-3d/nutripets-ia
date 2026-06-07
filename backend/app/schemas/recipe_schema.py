from pydantic import BaseModel
from typing import Literal


class RecipeSchema(BaseModel):

    id: int | None = None

    title: str

    description: str | None = None

    preparation: str

    preparation_time: int | None = None

    difficulty: Literal[
        "Fácil",
        "Media",
        "Difícil"
    ]

    calories: int | None = None