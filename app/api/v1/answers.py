from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.answer import Answer as AnswerModel
from app.schemas.answer import AnswerCreate, AnswerRead
from app.services.answer_service import create_answer as create_answer_service, get_answers_by_user
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=AnswerRead, status_code=201)
def create_answer(answer_in: AnswerCreate, db: Session = Depends(get_db)):
    return create_answer_service(db, answer_in)

@router.get("/user/{user_id}", response_model=List[AnswerRead])
def list_answers_for_user(user_id: int, db: Session = Depends(get_db)):
    answers = get_answers_by_user(db, user_id)
    if not answers:
        raise HTTPException(status_code=404, detail="No answers found for user")
    return answers
