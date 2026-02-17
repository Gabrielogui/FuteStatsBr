from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from src.models.enums import CompetitionTypeEnum, RegionEnum

class CompetitionBase(BaseModel):
    name            : str = Field(..., description="O nome da competição", examples=["Brasileirão Serie A"])
    competition_type: CompetitionTypeEnum = Field(..., description="O tipo da competição")
    region          : RegionEnum = Field(..., description="A região da competição")
    description     : str = Field(None, description="A descrição da competição")

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionUpdate(CompetitionBase):
    name            : Optional[str] = None
    competition_type: Optional[CompetitionTypeEnum] = None
    region          : Optional[RegionEnum] = None
    description     : Optional[str] = None

class CompetitionRead(CompetitionBase):
    id        : UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)