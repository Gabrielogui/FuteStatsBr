from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.team_repository import TeamRepository
from src.schemas.team_schemas import TeamCreate, TeamUpdate
from src.models.team_model import Team

class TeamService:
    def __init__(self, session: AsyncSession):
        self.repository = TeamRepository(session)

    async def list_teams(self, skip: int = 0, limit: int = 100) -> List[Team]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def get_team(self, team_id: UUID) -> Optional[Team]:
        return await self.repository.get_by_id(team_id)

    async def get_team_with_stadium(self, team_id: UUID) -> Optional[Team]:
        return await self.repository.get_by_id_with_stadium(team_id)

    async def create_new_team(self, team_data: TeamCreate) -> Team:
        existing = await self.repository.get_by_name(team_data.name)
        if existing:
            # Esta lógica será capturada pelo router para retornar 400
            raise ValueError(f"Equipa com o nome {team_data.name} já existe.")
        
        return await self.repository.create(team_data)

    async def update_team_info(self, team_id: UUID, team_data: TeamUpdate) -> Optional[Team]:
        db_team = await self.repository.get_by_id(team_id)
        if not db_team:
            return None
        
        return await self.repository.update(db_team, team_data)

    async def remove_team(self, team_id: UUID) -> bool:
        return await self.repository.delete(team_id)