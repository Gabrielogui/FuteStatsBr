from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.models.edition_model import Phase
from src.repository.base_repository import BaseRepository

class PhaseRepository(BaseRepository[Phase]):
    def __init__(self, session: AsyncSession):
        super().__init__(Phase, session)

    async def get_by_edition(self, edition_id: uuid.UUID) -> Sequence[Phase]:
        query = select(Phase).where(Phase.edition_id == edition_id).order_by(Phase.order.asc())
        result = await self.session.execute(query)
        return result.scalars().all()