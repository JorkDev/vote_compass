from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.question import Question as QuestionModel
from app.schemas.question import QuestionCreate, QuestionRead
from app.services.question_service import get_questions, create_question
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[QuestionRead])
def list_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_questions(db, skip, limit)

@router.get("/{question_id}", response_model=QuestionRead)
def read_question(question_id: str, db: Session = Depends(get_db)):
    q = db.query(QuestionModel).get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.post("/", response_model=QuestionRead, status_code=201)
def create_question_endpoint(q_in: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, q_in)

@router.put("/{question_id}", response_model=QuestionRead)
def update_question(question_id: str, q_in: QuestionCreate, db: Session = Depends(get_db)):
    q = db.query(QuestionModel).get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    for field, value in q_in.dict().items():
        setattr(q, field, value)
    db.commit()
    db.refresh(q)
    return q

@router.delete("/{question_id}", status_code=204)
def delete_question(question_id: str, db: Session = Depends(get_db)):
    q = db.query(QuestionModel).get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
