from typing import Any, Dict
from pydantic import BaseModel, constr

class PartyBase(BaseModel):
    party_id: constr(min_length=1)
    name: str
    faction: str
    description: str | None = None
    inscription_date: str | None = None  # ISO date
    founder: str | None = None
    current_leader: str | None = None
    presidential_candidate: str | None = None
    positions: Dict[str, Any]

class PartyCreate(PartyBase):
    pass

class PartyRead(PartyBase):
    class Config:
        orm_mode = True
