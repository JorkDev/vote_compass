from sqlalchemy.orm import Session
import uuid
from app.db.models.result import Result
from app.schemas.result import ResultCreate

def create_result(db: Session, r_in: ResultCreate):
    db_r = Result(user_id=r_in.user_id, data=r_in.data)
    db.add(db_r)
    db.commit()
    db.refresh(db_r)
    return db_r

def get_result_by_token(db: Session, token: uuid.UUID):
    return db.query(Result).filter(Result.token == token).first()
