from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
class PhaseCreate(BaseModel):
    name      : str = Field(..., min_length=2, max_length=100, example="Fase Única")
    order     : int = Field(..., gt=0, example=1, description="Ordem cronológica da fase no campeonato")
    edition_id: UUID

class PhaseResponse(BaseModel):
    id        : UUID
    name      : str
    order     : int
    edition_id: UUID

    class Config:
        from_attributes = True