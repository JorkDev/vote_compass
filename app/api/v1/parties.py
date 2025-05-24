from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.party import Party as PartyModel
from app.schemas.party import PartyCreate, PartyRead
from app.services.party_service import get_parties, create_party
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[PartyRead])
def list_parties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_parties(db, skip, limit)

@router.get("/{party_id}", response_model=PartyRead)
def read_party(party_id: str, db: Session = Depends(get_db)):
    p = db.query(PartyModel).get(party_id)
    if not p:
        raise HTTPException(status_code=404, detail="Party not found")
    return p

@router.post("/", response_model=PartyRead, status_code=201)
def create_party_endpoint(p_in: PartyCreate, db: Session = Depends(get_db)):
    return create_party(db, p_in)

@router.put("/{party_id}", response_model=PartyRead)
def update_party(party_id: str, p_in: PartyCreate, db: Session = Depends(get_db)):
    p = db.query(PartyModel).get(party_id)
    if not p:
        raise HTTPException(status_code=404, detail="Party not found")
    for field, value in p_in.dict().items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{party_id}", status_code=204)
def delete_party(party_id: str, db: Session = Depends(get_db)):
    p = db.query(PartyModel).get(party_id)
    if not p:
        raise HTTPException(status_code=404, detail="Party not found")
    db.delete(p)
    db.commit()
