from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel
import uuid

class PartyScore(BaseModel):
    party: str
    score: float

class Coord(BaseModel):
    label: str
    x: float
    y: float

class ResultData(BaseModel):
    matches: List[PartyScore]
    coords: List[Coord]

class ResultRead(BaseModel):
    id: int
    user_id: int
    token: uuid.UUID
    created_at: datetime
    data: ResultData

    class Config:
        orm_mode = True
