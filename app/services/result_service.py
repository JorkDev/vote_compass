from sqlalchemy.orm import Session
from app.db.models.result import Result as ResultModel

def get_result_by_token(db: Session, token: str) -> ResultModel:
    return db.query(ResultModel).filter(ResultModel.token == token).first()
