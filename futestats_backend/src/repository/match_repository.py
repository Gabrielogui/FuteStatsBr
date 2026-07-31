from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.models.match_model import Match
from src.models.edition_model import Round
from src.models.enums import MatchStatusEnum
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

    