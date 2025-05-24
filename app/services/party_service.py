from sqlalchemy.orm import Session
from app.db.models.party import Party
from app.schemas.party import PartyCreate

def get_parties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Party).offset(skip).limit(limit).all()

def create_party(db: Session, p_in: PartyCreate):
    db_p = Party(**p_in.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p
