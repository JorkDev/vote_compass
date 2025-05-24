from datetime import datetime
from pydantic import BaseModel

class AnswerBase(BaseModel):
    user_id: int
    question_id: str
    choice: int

class AnswerCreate(AnswerBase):
    pass

class AnswerRead(AnswerBase):
    id: int
    answered_at: datetime

    class Config:
        orm_mode = True
