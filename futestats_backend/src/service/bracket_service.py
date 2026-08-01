from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID


from src.models.enums import EditionFormatEnum

from src.repository.edition_repository import EditionRepository
from src.repository.phase_repository import PhaseRepository
from src.repository.match_repository import MatchRepository
from src.engine.bracket_calculator import BracketCalculator
from src.schemas.bracket_schemas import BracketResponse, KnockoutPhaseResponse

# TODO: NÃO PERMITIR QUE UMA COMPETIÇÃO DE PONTOS CORRIDOS RETORNE EM MATA-MATA

class BracketService:
    def __init__(self, session: AsyncSession):
        self.session      = session
        self.edition_repo = EditionRepository(session)
        self.phase_repo   = PhaseRepository(session)
        self.match_repo   = MatchRepository(session)
        self.calculator   = BracketCalculator()

    async def get_edition_bracket(self, edition_id: UUID) -> BracketResponse:
        """Retorna a árvore completa de mata-mata de uma edição (todas as fases eliminatórias)."""
        edition = await self.edition_repo.get_by_id(edition_id)
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Edição não encontrada."
            )

        if edition.format == EditionFormatEnum.POINTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Edições no formato Pontos Corridos não possuem chaveamento. Utilize o endpoint GET /editions/{ id}/table."
            )

        phases = await self.phase_repo.get_by_edition(edition_id)
        calculated_phases: List[KnockoutPhaseResponse] = []

        for phase in phases:
            matches = await self.match_repo.get_matches_by_phase_with_relations(phase.id)
            
            # Se a fase possui jogos, processa os confrontos eliminatórios
            if matches:
                phase_bracket = self.calculator.calculate_phase_confrontos(
                    phase_id=phase.id,
                    phase_name=phase.name,
                    order=phase.order,
                    matches=matches
                )
                calculated_phases.append(phase_bracket)

        return BracketResponse(
            edition_id=edition.id,
            edition_name=edition.name,
            year=edition.year,
            phases=calculated_phases
        )

    async def get_phase_bracket(self, phase_id: UUID) -> KnockoutPhaseResponse:
        """Retorna os confrontos mata-mata de uma fase específica (ex: Quartas de Final)."""
        phase = await self.phase_repo.get_by_id(phase_id)
        if not phase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fase não encontrada."
            )

        matches = await self.match_repo.get_finished_matches_by_phase(phase_id, with_relations=True)
        
        return self.calculator.calculate_phase_confrontos(
            phase_id=phase.id,
            phase_name=phase.name,
            order=phase.order,
            matches=matches
        )