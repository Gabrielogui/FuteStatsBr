from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from src.repository.base_repository import BaseRepository
from src.models.team_model import Team

class TeamRepository(BaseRepository[Team]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Team, session)

    async def get_by_name(self, name: str) -> Optional[Team]:
        query = select(self.model).where(self.model.name == name).options(joinedload(Team.stadium))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_teams_with_stadiums(self):
        query = select(self.model).options(joinedload(Team.stadium))
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id_with_stadium(self, team_id: UUID) -> Optional[Team]:
        query = (
            select(self.model)
            .where(self.model.id == team_id)
            .options(joinedload(Team.stadium)) # Carregamento antecipado (Eager Loading)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_teams_by_stadium(self, stadium_id: UUID) -> List[Team]:
        query = select(self.model).where(self.model.stadium_id == stadium_id)
        result = await self.session.execute(query)
        return result.scalars().all()