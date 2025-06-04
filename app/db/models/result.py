import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON, text
from sqlalchemy.sql import func           # ← add this
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, nullable=False)            # e.g. { "matches": [...], "coords": [...] }
    token = Column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
