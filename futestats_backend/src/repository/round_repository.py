from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import uuid

from src.models.edition_model import Round
from src.models.match_model import Match
from src.repository.base_repository import BaseRepository

class RoundRepository(BaseRepository[Round]):
    def __init__(self, session: AsyncSession):
        super().__init__(Round, session)

    async def get_with_matches(self, round_id: uuid.UUID) -> Optional[Round]:
        """Busca uma rodada trazendo jogos, times mandante/visitante e estádio."""
        query = (
            select(Round)
            .where(Round.id == round_id)
            .options(
                selectinload(Round.matches).options(
                    selectinload(Match.home_team),
                    selectinload(Match.away_team),
                    selectinload(Match.stadium)
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_phase(self, phase_id: uuid.UUID) -> List[Round]:
        """Lista todas as rodadas de uma determinada fase ordenadas pelo número."""
        query = (
            select(Round)
            .where(Round.phase_id == phase_id)
            .options(selectinload(Round.matches).options(
                selectinload(Match.home_team),
                selectinload(Match.away_team),
                selectinload(Match.stadium)
            ))
            .order_by(Round.number.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())