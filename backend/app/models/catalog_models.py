from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Species(Base):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class LifeStage(Base):
    __tablename__ = "life_stages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stage_name: Mapped[str] = mapped_column(String(50), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)