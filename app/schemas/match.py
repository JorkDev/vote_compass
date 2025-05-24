from typing import Dict, List
from pydantic import BaseModel

class MatchRequest(BaseModel):
    answers: Dict[str, int]
    weights: Dict[str, int]

class PartyScore(BaseModel):
    party: str
    score: float

class MatchResponse(BaseModel):
    matches: List[PartyScore]
