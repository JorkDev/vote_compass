import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.result import Result as ResultModel
from app.schemas.result import ResultRead
from app.services.result_service import get_result_by_token
from app.db.session import get_db
from app.schemas.match import MatchRequest  # add this import
from app.db.models.party import Party as PartyModel  # add this import
from app.db.models.question import Question as QuestionModel  # add this import
from app.services.matcher import match_user_to_parties  # add this import
from app.services.advanced_model import compute_latent_positions  # add this import

router = APIRouter()

@router.post("/", response_model=ResultRead, status_code=201)
def compute_and_store_result(
    req: MatchRequest, db: Session = Depends(get_db)
):
    # 1) Load all parties from the DB
    party_objs = db.query(PartyModel).all()

    # Convert ORM models into simple dicts for matching & coords
    parties_for_match = []
    for p in party_objs:
        parties_for_match.append({
            "name": p.name,
            "positions": p.positions  # assumes JSON column
        })

    # 2) Compute match scores
    matches = match_user_to_parties(req.answers, req.weights, parties_for_match)

    # 3) Load questions and convert to dicts
    question_objs = db.query(QuestionModel).all()
    questions_for_coords = []
    for q in question_objs:
        questions_for_coords.append({
            "id": q.id,
            "dimension": [q.dimension] if isinstance(q.dimension, str) else q.dimension
        })

    # 4) Compute latent positions using the same dicts
    user_coord, party_coords = compute_latent_positions(
        req.answers, questions_for_coords, parties_for_match
    )

    # 5) Build payload
    payload = {
        "matches": matches,
        "coords": [user_coord] + party_coords
    }

    # 6) Persist
    # Only store user_id if present (for anonymous users, allow null)
    db_r = ResultModel(user_id=req.user_id if req.user_id is not None else 0, data=payload)
    db.add(db_r)
    db.commit()
    db.refresh(db_r)

    return db_r

@router.get("/{token}", response_model=ResultRead)
def read_result(token: uuid.UUID, db: Session = Depends(get_db)):
    result = get_result_by_token(db, token)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result
