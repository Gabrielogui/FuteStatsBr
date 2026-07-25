from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.models.edition_model import Edition
from src.repository.base_repository import BaseRepository

class EditionRepository(BaseRepository[Edition]):
    def __init__(self, session: AsyncSession):
        super().__init__(Edition, session)

    async def get_with_relations(self, edition_id: UUID) -> Optional[Edition]:
        """Carrega uma edição juntamente com a competição, times participantes e fases."""
        query = (
            select(Edition)
            .where(Edition.id == edition_id)
            .options(
                selectinload(Edition.competition),
                selectinload(Edition.teams),
                selectinload(Edition.phases)
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_competition(self, competition_id: UUID) -> Sequence[Edition]:
        """Lista todas as edições de uma competição ordenadas pelo ano decrescente."""
        query = (
            select(Edition)
            .where(Edition.competition_id == competition_id)
            .options(
                selectinload(Edition.teams),
                selectinload(Edition.phases),
                selectinload(Edition.competition)
            )
            .order_by(Edition.year.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()