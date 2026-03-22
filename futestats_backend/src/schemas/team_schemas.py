from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from src.schemas.stadium_schemas import StadiumRead
from src.schemas.photo_schemas import PhotoRead

from src.models.enums import StateEnum, ColorEnum

class TeamBase(BaseModel):
    name       : str = Field(..., description="O nome da equipe", example="Esporte Clube Vitória")
    short_name : Optional[str] = Field(..., description="O nome abreviado da equipe", example="Vitória")
    sigla      : Optional[str] = Field(..., description="A sigla da equipe", example="VIT")
    city       : Optional[str] = Field(..., description="A cidade da equipe", example="Salvador")
    state      : Optional[StateEnum] = Field(..., description="O estado da equipe", example="BA")

    colors        : Optional[List[str]] = Field(..., description="As cores da equipe", example=["#000000", "#FFFFFF"])
    alcunha       : Optional[str] = Field(..., description="A alcunha da equipe", example="Leão da Barra")
    alcunha_color : Optional[str] = Field(..., description="As cores da alcunha da equipe", example="Rubro-negro")
    year          : Optional[int] = Field(..., description="O ano de fundação da equipe", example="1900")
    mascot        : Optional[str] = Field(..., description="A mascote da equipe", example="Leão")
    description   : Optional[str] = Field(..., description="A descrição da equipe", example="Uma equipe de futebol de determinada cidade do Brasil")


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

    subscribers_count: Optional[int] = Field(None, description="A quantidade de assinantes da equipe", example=1000)

    images: list[PhotoRead] = []

    model_config = ConfigDict(from_attributes=True)

class TeamReadWithStadium(TeamRead):
    stadium: Optional[StadiumRead] = None