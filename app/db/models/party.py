from sqlalchemy import Column, String, Text, Date, JSON
from app.db.base import Base

class Party(Base):
    __tablename__ = "parties"

    party_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    faction = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    inscription_date = Column(Date, nullable=True)
    founder = Column(String, nullable=True)
    current_leader = Column(String, nullable=True)
    presidential_candidate = Column(String, nullable=True)
    positions = Column(JSON, nullable=False)      # map question_id → { value, source }
