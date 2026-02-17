from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.base_repository import BaseRepository
from src.models.stadium_model import Stadium

class StadiumRepository(BaseRepository[Stadium]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Stadium, session)

    async def get_by_name(self, name: str) -> Optional[Stadium]:
        query = select(self.model).where(self.model.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()