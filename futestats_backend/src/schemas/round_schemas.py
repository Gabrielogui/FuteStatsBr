from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.models.enums import MatchStatusEnum
from src.schemas.stadium_schemas import StadiumSimpleResponse
from src.schemas.team_schemas import TeamSimpleResponse

# DTO do jogo enviado DENTRO da criacao da rodada
class MatchInRoundCreate(BaseModel):
    home_team_id: UUID
    away_team_id: UUID
    stadium_id  : Optional[UUID] = None
    date        : Optional[datetime] = None
    home_score  : int = Field(default=0, ge=0)
    away_score  : int = Field(default=0, ge=0)
    status      : MatchStatusEnum = MatchStatusEnum.SCHEDULED


# DTO principal de cadastro da Rodada com seus jogos
class RoundCreate(BaseModel):
    number    : int = Field(..., gt=0, description="Número ordinal da rodada (ex: 1)")
    name      : Optional[str] = Field(None, description="Nome customizado (ex: '1ª Rodada')")
    phase_id  : UUID
    edition_id: UUID
    matches   : List[MatchInRoundCreate] = Field(default_factory=list)


# Resposta do Jogo dentro da Rodada
class MatchInRoundResponse(BaseModel):
    id          : UUID
    date        : Optional[datetime] = None
    home_score  : int
    away_score  : int
    status      : MatchStatusEnum

    home_team: TeamSimpleResponse
    away_team: TeamSimpleResponse
    stadium  : Optional[StadiumSimpleResponse] = None

    class Config:
        from_attributes = True


# Resposta Completa da Rodada
class RoundResponse(BaseModel):
    id      : UUID
    number  : int
    name    : Optional[str]
    phase_id: UUID
    matches : List[MatchInRoundResponse] = []

    class Config:
        from_attributes = True