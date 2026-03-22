from typing import Optional, override
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.base_repository import BaseRepository
from src.models.stadium_model import Stadium
from uuid import UUID

class StadiumRepository(BaseRepository[Stadium]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Stadium, session)

    @override
    async def get_all(self, skip = 0, limit = 100):
        query = (
            select(self.model)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Stadium.images)
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    @override
    async def get_by_id(self, id: UUID):
        query = (
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(Stadium.images))
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Stadium]:
        query = select(self.model).where(self.model.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()