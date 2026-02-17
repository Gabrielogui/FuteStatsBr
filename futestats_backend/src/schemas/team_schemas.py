from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.schemas.stadium_schemas import StadiumRead

class TeamBase(BaseModel):
    name       : str = Field(..., description="O nome da equipe", example="Esporte Clube Vitória")
    short_name : Optional[str] = Field(..., description="O nome abreviado da equipe", example="Vitória")
    alcunha    : Optional[str] = Field(..., description="A alcunha da equipe", example="Leão da Barra")
    year       : Optional[int] = Field(..., description="O ano de fundação da equipe", example="1900")
    description: Optional[str] = Field(..., description="A descrição da equipe", example="Uma equipe de futebol de determinada cidade do Brasil")

class TeamCreate(TeamBase):
    stadium_id: Optional[UUID] = None

class TeamUpdate(TeamBase):
    name: Optional[str]
    short_name: Optional[str]
    alcunha: Optional[str]
    year: Optional[int]
    description: Optional[str]

class TeamRead(TeamBase):
    id: UUID
    stadium_id: Optional[UUID]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TeamReadWithStadium(TeamRead):
    stadium: Optional[StadiumRead] = None