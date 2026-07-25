from typing import List, Optional
from sqlalchemy import select
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
        until_round: Optional[int] = None
    ) -> List[Match]:
        """Busca todas as partidas finalizadas de uma edição, filtrando até uma rodada opcional."""
        query = (
            select(Match)
            .join(Match.round, isouter=True)
            .where(Match.edition_id == edition_id)
            .where(Match.status == MatchStatusEnum.FINISHED)
        )

        if until_round is not None:
            query = query.where(Round.number <= until_round)

        result = await self.session.execute(query)
        return list(result.scalars().all())