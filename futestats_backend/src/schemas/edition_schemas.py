from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from uuid import UUID
from src.models.enums import EditionFormatEnum
from src.schemas.comepetition_schemas import CompetitionRead
from src.schemas.phase_schemas import PhaseResponse
from src.schemas.team_schemas import TeamSimpleResponse 

class EditionCreate(BaseModel):
    name  : str = Field(..., min_length=2, max_length=100, example="Campeonato Brasileiro Série A 2026")
    year  : int = Field(..., gt=1900, example=2026)
    format: EditionFormatEnum
    competition_id : UUID
    relegated_count: Optional[int] = Field(None, ge=0, description="Número de rebaixados na edição (pode ser Nulo)")
    rules_config: Optional[Dict[str, Any]] = Field(
        None, 
        example={"g4_direct": 4, "g6_pre": 2, "sulamericana": [7, 8, 9, 10, 11, 12]}
    )
    team_ids: Optional[List[UUID]] = Field(default_factory=list, description="Lista inicial de times participantes")

class EditionUpdate(BaseModel):
    name  : Optional[str] = None
    year  : Optional[int] = None
    format: Optional[EditionFormatEnum] = None
    relegated_count: Optional[int] = None
    rules_config   : Optional[Dict[str, Any]] = None

class EditionTeamsUpdate(BaseModel):
    team_ids: List[UUID] = Field(..., description="Lista de IDs dos times a serem associados à edição")

class EditionResponse(BaseModel):
    id    : UUID
    name  : str
    year  : int
    format: EditionFormatEnum
    competition_id : UUID
    relegated_count: Optional[int] = None
    rules_config   : Optional[Dict[str, Any]] = None
    
    competition: Optional[CompetitionRead] = None
    teams      : List[TeamSimpleResponse] = []
    phases     : List[PhaseResponse] = []

    class Config:
        from_attributes = True