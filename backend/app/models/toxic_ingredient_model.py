from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.core.database import Base


class ToxicIngredient(Base):

    __tablename__ = "toxic_ingredients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    aliases = Column(
        Text,
        nullable=True
    )

    danger_level = Column(
        String(50),
        nullable=False
    )

    symptoms = Column(
        Text,
        nullable=False
    )

    action_required = Column(
        Text,
        nullable=False
    )