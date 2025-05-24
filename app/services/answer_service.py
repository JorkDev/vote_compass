from sqlalchemy.orm import Session
from app.db.models.answer import Answer
from app.schemas.answer import AnswerCreate

def create_answer(db: Session, a_in: AnswerCreate):
    db_a = Answer(**a_in.dict())
    db.add(db_a)
    db.commit()
    db.refresh(db_a)
    return db_a

def get_answers_by_user(db: Session, user_id: int):
    return db.query(Answer).filter(Answer.user_id == user_id).all()
