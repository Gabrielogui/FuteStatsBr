from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db.session import get_db
from src.service.team_service import TeamService
from src.schemas.team_schemas import TeamCreate, TeamRead, TeamReadWithStadium, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/", response_model=List[TeamRead])
async def get_teams(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    service = TeamService(db)
    return await service.list_teams(skip, limit)

@router.get("/{team_id}", response_model=TeamReadWithStadium)
async def get_team_detail(team_id: UUID, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    team = await service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    return team

@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(team_in: TeamCreate, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    try:
        return await service.create_new_team(team_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{team_id}", response_model=TeamRead)
async def update_team(team_id: UUID, team_in: TeamUpdate, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    updated_team = await service.update_team_info(team_id, team_in)
    if not updated_team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    return updated_team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: UUID, db: AsyncSession = Depends(get_db)):
    service = TeamService(db)
    success = await service.remove_team(team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")