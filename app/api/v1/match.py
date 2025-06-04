from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.match import MatchRequest, MatchResponse, PartyScore
from app.services.matcher import match_user_to_parties
from app.db.models.party import Party as PartyModel
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=MatchResponse)
def match_user(req: MatchRequest, db: Session = Depends(get_db)):
    # load parties from the database and turn them into simple dicts
    party_objs = db.query(PartyModel).all()
    parties: List[Dict[str, Any]] = [
        {"name": p.name, "positions": p.positions}
        for p in party_objs
    ]

    # calculate scores
    scores = match_user_to_parties(req.answers, req.weights, parties)

    # wrap in your response schema
    return {"matches": [PartyScore(**s) for s in scores]}
