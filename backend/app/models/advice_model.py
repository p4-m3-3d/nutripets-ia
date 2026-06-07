from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.core.database import Base


class Advice(Base):
    __tablename__ = "advice"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    content = Column(Text, nullable=False)