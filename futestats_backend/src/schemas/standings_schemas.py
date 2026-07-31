from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from src.schemas.team_schemas import TeamSimpleResponse

from src.models.enums import StandingsZoneEnum

class TeamStatsAccumulator(BaseModel):
    team: TeamSimpleResponse

    points         : int = 0
    played         : int = 0
    wins           : int = 0
    draws          : int = 0
    losses         : int = 0
    goals_for      : int = 0
    goals_against  : int = 0
    goal_difference: int = 0
    win_rate       : float = 0.0 # Aproveitamento %
    zone           : StandingsZoneEnum = StandingsZoneEnum.NEUTRAL

class TeamStandingResponse(BaseModel):
    position: int

    team: TeamSimpleResponse

    points         : int
    played         : int
    wins           : int
    draws          : int
    losses         : int
    goals_for      : int
    goals_against  : int
    goal_difference: int
    win_rate       : float
    zone           : StandingsZoneEnum

class StandingsTableResponse(BaseModel):
    edition_id  : UUID
    edition_name: str
    year        : int
    start_round : Optional[int] = None
    until_round : Optional[int] = None
    standings   : List[TeamStandingResponse]