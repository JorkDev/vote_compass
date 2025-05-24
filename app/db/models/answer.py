from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String, nullable=False)
    choice = Column(Integer, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships (optional)
    # user = relationship("User", back_populates="answers")
