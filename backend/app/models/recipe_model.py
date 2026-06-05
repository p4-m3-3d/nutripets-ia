from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from app.core.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(Text)

    preparation = Column(Text, nullable=False)

    preparation_time = Column(Integer)

    difficulty = Column(String(20))

    image_url = Column(String(255))

    species_id = Column(Integer, ForeignKey("species.id"))

    life_stage_id = Column(Integer, ForeignKey("life_stages.id"))

    category_id = Column(Integer, ForeignKey("categories.id"))

    calories = Column(Integer)