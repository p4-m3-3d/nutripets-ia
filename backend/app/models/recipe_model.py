from typing import Optional
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    preparation: Mapped[str] = mapped_column(Text, nullable=False)
    preparation_time: Mapped[Optional[int]] = mapped_column(nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    calories: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Llaves Foráneas numéricas explícitas
    species_id: Mapped[Optional[int]] = mapped_column(ForeignKey("species.id"), nullable=True)
    life_stage_id: Mapped[Optional[int]] = mapped_column(ForeignKey("life_stages.id"), nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)