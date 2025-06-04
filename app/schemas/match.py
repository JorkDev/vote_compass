from typing import Dict, List, Optional
from pydantic import BaseModel

class MatchRequest(BaseModel):
    user_id: Optional[int] = None  # user_id is now optional
    answers: Dict[str, int]
    weights: Dict[str, int]

class PartyScore(BaseModel):
    party: str
    score: float

class MatchResponse(BaseModel):
    matches: List[PartyScore]

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
    token: str
    created_at: str
    data: ResultData

    class Config:
        orm_mode = True
