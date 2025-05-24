from typing import List
from pydantic import BaseModel

class QuestionBase(BaseModel):
    id: str
    text: str
    options: List[str]
    dimension: str
    topic: str
    additional_info: str | None = None

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    class Config:
        orm_mode = True
