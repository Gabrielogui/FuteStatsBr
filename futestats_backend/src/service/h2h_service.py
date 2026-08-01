from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.repository.match_repository import MatchRepository
from src.repository.team_repository import TeamRepository
from src.engine.h2h_calculator import H2HCalculator
from src.schemas.h2h_schemas import H2HSummaryResponse

class H2HService:
    def __init__(self, session: AsyncSession):
        self.session    = session
        self.match_repo = MatchRepository(session)
        self.team_repo  = TeamRepository(session)

    async def get_head_to_head_summary(
        self,
        team1_id: UUID,
        team2_id: UUID,
        competition_id: Optional[UUID] = None,
        stadium_id: Optional[UUID] = None,
        only_home_team_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> H2HSummaryResponse:
        
        if team1_id == team2_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selecione dois times diferentes para consultar o confronto direto."
            )

        team1 = await self.team_repo.get_by_id(team1_id)
        team2 = await self.team_repo.get_by_id(team2_id)

        if not team1 or not team2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Um ou ambos os times informados não foram encontrados."
            )

        matches = await self.match_repo.get_h2h_matches(
            team1_id=team1_id,
            team2_id=team2_id,
            competition_id=competition_id,
            stadium_id=stadium_id,
            only_home_team_id=only_home_team_id,
            start_date=start_date,
            end_date=end_date
        )

        calculator = H2HCalculator(team1, team2)
        return calculator.calculate(matches)
    