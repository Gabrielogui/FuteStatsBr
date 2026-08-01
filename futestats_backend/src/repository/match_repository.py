from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from src.models.match_model import Match
from src.models.edition_model import Round
from src.models.enums import MatchStatusEnum
from src.models.edition_model import Edition

from src.repository.base_repository import BaseRepository

class MatchRepository(BaseRepository[Match]):
    def __init__(self, session: AsyncSession):
        super().__init__(Match, session)

    async def get_finished_matches_by_edition(
        self, 
        edition_id: UUID, 
        start_round: Optional[int] = None,
        until_round: Optional[int] = None,
    ) -> List[Match]:
        """Busca todas as partidas finalizadas de uma edição, filtrando até uma rodada opcional."""
        query = (
            select(Match)
            .join(Match.round, isouter=True)
            .where(Match.edition_id == edition_id)
            .where(Match.status == MatchStatusEnum.FINISHED)
        )

        if (until_round or start_round) is not None:  
            if until_round is not None and start_round is None:
                query = query.where(Round.number <= until_round)
            elif until_round is None and start_round is not None:
                query = query.where(Round.number >= start_round)
            else:
                query = query.where(Round.number.between(start_round, until_round))
            

        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def get_finished_matches_by_phase(self, phase_id: UUID, with_relations: bool = False) -> List[Match]:
        """Busca partidas finalizadas de uma fase específica (ex: Grupo A do Paulistão)."""
        query = (
            select(Match)
            .where(Match.phase_id == phase_id)
            .where(Match.status == MatchStatusEnum.FINISHED)
        )

        if with_relations:
            query = query.options(
                selectinload(Match.home_team),
                selectinload(Match.away_team),
                selectinload(Match.stadium),
                selectinload(Match.round)
            )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_h2h_matches(
        self,
        team1_id: UUID,
        team2_id: UUID,
        competition_id: Optional[UUID] = None,
        stadium_id: Optional[UUID] = None,
        only_home_team_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Match]:
        """
        Busca todas as partidas finalizadas entre dois times aplicando filtros dinâmicos.
        """
        # Jogos onde os times se enfrentaram (independente de mandante/visitante)
        query = (
            select(Match)
            .where(Match.status == MatchStatusEnum.FINISHED)
            .where(
                ((Match.home_team_id == team1_id) & (Match.away_team_id == team2_id)) |
                ((Match.home_team_id == team2_id) & (Match.away_team_id == team1_id))
            )
        )

        # Filtro: Apenas partidas onde um time específico jogou como mandante
        if only_home_team_id:
            query = query.where(Match.home_team_id == only_home_team_id)

        # Filtro: Competição
        if competition_id:
            query = query.join(Match.edition).where(Edition.competition_id == competition_id)

        # Filtro: Estádio
        if stadium_id:
            query = query.where(Match.stadium_id == stadium_id)

        # Filtro: Intervalo de Datas
        if start_date:
            query = query.where(Match.date >= start_date)
        if end_date:
            query = query.where(Match.date <= end_date)

        # Previne erro MissingGreenlet carregando as relações necessárias para os Schemas
        query = query.options(
            selectinload(Match.home_team),
            selectinload(Match.away_team),
            selectinload(Match.stadium),
            selectinload(Match.edition),
            selectinload(Match.phase),
            selectinload(Match.round)
        ).order_by(Match.date.desc())

        result = await self.session.execute(query)
        return list(result.scalars().all())   
    