from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.base_repository import BaseRepository
from src.models.competition_model import Competition
from src.models.enums import CompetitionTypeEnum

class CompetitionRepository(BaseRepository[Competition]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Competition, session)

    async def get_by_type(self, comp_type: CompetitionTypeEnum) -> Sequence[Competition]:
        query = select(self.model).where(self.model.competition_type == comp_type)
        result = await self.session.execute(query)
        return result.scalars().all()