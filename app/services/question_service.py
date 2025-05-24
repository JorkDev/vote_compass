from sqlalchemy.orm import Session
from app.db.models.question import Question
from app.schemas.question import QuestionCreate

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()

def create_question(db: Session, q_in: QuestionCreate):
    db_q = Question(**q_in.dict())
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    return db_q
