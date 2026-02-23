from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.stadium_repository import StadiumRepository
from src.schemas.stadium_schemas import StadiumCreate, StadiumUpdate
from src.models.stadium_model import Stadium

class StadiumService:
    def __init__(self, session: AsyncSession):
        self.repository = StadiumRepository(session)

    async def list_stadiums(self, skip: int = 0, limit: int = 100) -> List[Stadium]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def get_stadium(self, stadium_id: UUID) -> Optional[Stadium]:
        return await self.repository.get_by_id(stadium_id)

    async def create_new_stadium(self, stadium_data: StadiumCreate) -> Stadium:
        existing = await self.repository.get_by_name(stadium_data.name)
        if existing:
            raise ValueError(f"Estádio com o nome {stadium_data.name} já existe.")
        
        return await self.repository.create(stadium_data)

    async def update_stadium_info(self, stadium_id: UUID, stadium_data: StadiumUpdate) -> Optional[Stadium]:
        db_stadium = await self.repository.get_by_id(stadium_id)
        if not db_stadium:
            return None
        
        return await self.repository.update(db_stadium, stadium_data)

    async def remove_stadium(self, stadium_id: UUID) -> bool:
        return await self.repository.delete(stadium_id)