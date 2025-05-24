from sqlalchemy import Column, String, JSON, Text
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)         # e.g. ["Tot. desacuerdo", …]
    dimension = Column(String, nullable=False)     # e.g. "economic" or JSON if multi
    topic = Column(String, nullable=False)         # e.g. "taxes"
    additional_info = Column(Text, nullable=True)
