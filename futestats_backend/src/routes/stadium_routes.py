from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db.session import get_db
from src.service.stadium_service import StadiumService
from src.schemas.stadium_schemas import StadiumCreate, StadiumRead, StadiumUpdate

router = APIRouter(prefix="/stadiums", tags=["Stadiums"])

@router.get("/", response_model=List[StadiumRead])
async def get_stadiums(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    service = StadiumService(db)
    return await service.list_stadiums(skip, limit)

@router.get("/{stadium_id}", response_model=StadiumRead)
async def get_stadium_detail(stadium_id: UUID, db: AsyncSession = Depends(get_db)):
    service = StadiumService(db)
    stadium = await service.get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Estádio não encontrado")
    return stadium

@router.post("/", response_model=StadiumRead, status_code=status.HTTP_201_CREATED)
async def create_stadium(stadium_in: StadiumCreate, db: AsyncSession = Depends(get_db)):
    service = StadiumService(db)
    try:
        return await service.create_new_stadium(stadium_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{stadium_id}", response_model=StadiumRead)
async def update_stadium(stadium_id: UUID, stadium_in: StadiumUpdate, db: AsyncSession = Depends(get_db)):
    service = StadiumService(db)
    updated_stadium = await service.update_stadium_info(stadium_id, stadium_in)
    if not updated_stadium:
        raise HTTPException(status_code=404, detail="Estádio não encontrado")
    return updated_stadium

@router.delete("/{stadium_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stadium(stadium_id: UUID, db: AsyncSession = Depends(get_db)):
    service = StadiumService(db)
    success = await service.remove_stadium(stadium_id)
    if not success:
        raise HTTPException(status_code=404, detail="Estádio não encontrado")