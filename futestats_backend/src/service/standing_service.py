from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.models.enums import EditionFormatEnum

from src.schemas.standings_schemas import StandingsTableResponse

from src.repository.edition_repository import EditionRepository
from src.repository.match_repository import MatchRepository
from src.repository.phase_repository import PhaseRepository

from src.engine.standings_calculator import StandingsCalculator


class StandingsService:
    def __init__(self, session: AsyncSession):
        self.session      = session
        self.edition_repo = EditionRepository(session)
        self.match_repo   = MatchRepository(session)
        self.phase_repo   = PhaseRepository(session)


    async def calculate_edition_standings(
        self,
        edition_id: UUID,
        start_round: Optional[int] = None, 
        until_round: Optional[int] = None
    ) -> StandingsTableResponse:
        
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
            start_round=start_round,
            until_round=until_round,
        )

        # 3. Executa o cálculo através do Engine especializado
        calculator = StandingsCalculator(edition)
        standings  = calculator.calculate(matches)

        return StandingsTableResponse(
            edition_id=edition.id,
            edition_name=edition.name,
            year=edition.year,
            start_round=start_round,
            until_round=until_round,
            standings=standings
        )

    async def calculate_phase_standings(
        self, 
        phase_id: UUID
    ) -> StandingsTableResponse:
        """Calcula a tabela de classificação específica de uma FASE (ex: Grupo A, 1º Turno)."""

        
        phase = await self.phase_repo.get_by_id(phase_id)
        if not phase:
            raise HTTPException(status_code=404, detail="Fase não encontrada.")

        edition = await self.edition_repo.get_with_relations(phase.edition_id)

        if edition.format == EditionFormatEnum.KNOCKOUT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Edições no formato Mata-Mata não possuem tabela de classificação. Utilize o endpoint GET /editions/{ id }/bracket."
            )

        matches = await self.match_repo.get_finished_matches_by_phase(phase_id, with_relations=True)

        calculator = StandingsCalculator(edition)
        standings = calculator.calculate(matches)

        return StandingsTableResponse(
            edition_id=edition.id,
            edition_name=f"{edition.name} - {phase.name}",
            year=edition.year,
            standings=standings
        )