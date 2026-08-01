from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.models.enums import MatchStatusEnum
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.stadium_schemas import StadiumSimpleResponse

# |=======| JOGO DE MAIOR GOLEADA NO CONFRONTO |=======| 
class H2HBiggestWinResponse(BaseModel):
    match_id        : UUID
    date            : Optional[datetime]
    edition_name    : str
    home_team       : TeamSimpleResponse
    away_team       : TeamSimpleResponse
    home_score      : int
    away_score      : int
    score_difference: int

    class Config:
        from_attributes = True

# |=======| RESUMO DE PARTIDA INDIVIDUAL NO HISTÓRICO |=======|
class H2HMatchItemResponse(BaseModel):
    match_id          : UUID
    date              : Optional[datetime]
    edition_name      : str
    phase_name        : Optional[str] = None
    round_number      : Optional[int] = None
    home_team         : TeamSimpleResponse
    away_team         : TeamSimpleResponse
    stadium           : Optional[StadiumSimpleResponse] = None
    home_score        : int
    away_score        : int
    home_penalty_score: Optional[int] = None
    away_penalty_score: Optional[int] = None
    status            : MatchStatusEnum

    class Config:
        from_attributes = True

# |=======| RESPOSTA COMPLETA DO RETROSPECTO |=======|
class H2HSummaryResponse(BaseModel):
    team1: TeamSimpleResponse
    team2: TeamSimpleResponse
    
    # Estatísticas Acumuladas
    total_matches: int
    team1_wins   : int
    team2_wins   : int
    draws        : int
    
    # Gols e Saldos
    team1_goals    : int
    team2_goals    : int
    goal_difference: int # Saldo do Team 1 em relação ao Team 2
    
    # Aproveitamentos %
    team1_win_rate: float
    team2_win_rate: float
    
    # Maiores Goleadas
    biggest_win_team1: Optional[H2HBiggestWinResponse] = None
    biggest_win_team2: Optional[H2HBiggestWinResponse] = None
    
    # Histórico de Jogos
    matches: List[H2HMatchItemResponse]