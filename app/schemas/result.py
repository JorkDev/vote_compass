import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel

class ResultBase(BaseModel):
    user_id: int
    data: Dict[str, Any]

class ResultCreate(ResultBase):
    pass

class ResultRead(ResultBase):
    id: int
    token: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
