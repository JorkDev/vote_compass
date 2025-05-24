import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.result import Result as ResultModel
from app.schemas.result import ResultCreate, ResultRead
from app.services.result_service import create_result as create_result_service, get_result_by_token
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ResultRead, status_code=201)
def create_result(r_in: ResultCreate, db: Session = Depends(get_db)):
    return create_result_service(db, r_in)

@router.get("/{token}", response_model=ResultRead)
def read_result(token: uuid.UUID, db: Session = Depends(get_db)):
    result = get_result_by_token(db, token)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result
