from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class ToxicIngredient(Base):
    __tablename__ = "toxic_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    aliases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    danger_level: Mapped[str] = mapped_column(String(50), nullable=False)
    symptoms: Mapped[str] = mapped_column(Text, nullable=False)
    action_required: Mapped[str] = mapped_column(Text, nullable=False)