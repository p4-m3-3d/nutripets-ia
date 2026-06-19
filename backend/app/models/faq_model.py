from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class FAQ(Base):
    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)