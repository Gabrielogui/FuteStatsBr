from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.schemas.standings_schemas import StandingsTableResponse

from src.repository.edition_repository import EditionRepository
from src.repository.match_repository import MatchRepository

from src.engine.standings_calculator import StandingsCalculator


class StandingsService:
    def __init__(self, session: AsyncSession):
        self.session      = session
        self.edition_repo = EditionRepository(session)
        self.match_repo   = MatchRepository(session)

    async def calculate_edition_standings(self, edition_id: UUID, until_round: Optional[int] = None) -> StandingsTableResponse:
        
        # 1. Busca a edição e seus times via Repositório
        edition = await self.edition_repo.get_with_relations(edition_id)
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Edição não encontrada."
            )

        # 2. Busca partidas finalizadas via Repositório
        matches = await self.match_repo.get_finished_matches_by_edition(
            edition_id=edition_id, 
            until_round=until_round
        )

        # 3. Executa o cálculo através do Engine especializado
        calculator = StandingsCalculator(edition)
        standings  = calculator.calculate(matches)

        return StandingsTableResponse(
            edition_id=edition.id,
            edition_name=edition.name,
            year=edition.year,
            until_round=until_round,
            standings=standings
        )