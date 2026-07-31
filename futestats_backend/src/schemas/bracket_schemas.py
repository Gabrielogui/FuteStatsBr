from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.models.enums import MatchStatusEnum
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.stadium_schemas import StadiumSimpleResponse

# |=======| JOGO INDIVIDUAL NO CONFRONTO |=======|
class KnockoutMatchResponse(BaseModel):
    id          : UUID
    round_number: int # 1 = Ida, 2 = Volta, 3 = Desempate(Se tiver)
    date        : Optional[datetime] = None
    home_team   : TeamSimpleResponse
    away_team   : TeamSimpleResponse
    stadium     : Optional[StadiumSimpleResponse] = None
    home_score  : int
    away_score  : int

    home_penalty_score: Optional[int] = None
    away_penalty_score: Optional[int] = None

    status: MatchStatusEnum

# |=======| CONFRONTO / CHAVE (Ex: Vitória vs Bahia nas Quartas) |=======|
class ConfrontoResponse(BaseModel):
    confronto_id           : str # Ex: "VIT-x-BAH"
    team_a                 : TeamSimpleResponse
    team_b                 : TeamSimpleResponse
    matches                : List[KnockoutMatchResponse]
    aggregate_score_a      : int = 0
    aggregate_score_b      : int = 0
    penalties_score_a      : Optional[int] = None
    penalties_score_b      : Optional[int] = None
    winner_team_id         : Optional[UUID] = None # Time que avançou de fase
    is_decided_on_penalties: bool = False

# |=======| FASE DE MATA-MATA (Ex: Quartas de Final) |=======|
class KnockoutPhaseResponse(BaseModel):
    phase_id  : UUID
    phase_name: str # Ex: "Quartas de Final"
    order     : int
    confrontos: List[ConfrontoResponse]

# |=======| Árvore Completa da Copa (Oitavas -> Quartas -> Semi -> Final) |=======|
class BracketResponse(BaseModel):
    edition_id  : UUID
    edition_name: str
    year        : int
    phases      : List[KnockoutPhaseResponse]