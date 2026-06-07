from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from app.core.database import Base


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)