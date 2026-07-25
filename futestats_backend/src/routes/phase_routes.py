from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.db.session import get_db
from src.schemas.phase_schemas import PhaseCreate, PhaseResponse
from src.service.phase_service import PhaseService

router = APIRouter(prefix="/phases", tags=["Fases dos Campeonatos"])

@router.post("/", response_model=PhaseResponse, status_code=status.HTTP_201_CREATED)
async def create_phase(
    payload: PhaseCreate,
    db: AsyncSession = Depends(get_db)
):
    service = PhaseService(db)
    return await service.create_phase(payload)

@router.get("/{phase_id}", response_model=PhaseResponse)
async def get_phase(
    phase_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = PhaseService(db)
    return await service.get_by_id(phase_id)

@router.get("/edition/{edition_id}", response_model=List[PhaseResponse])
async def get_phases_by_edition(
    edition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = PhaseService(db)
    return await service.get_by_edition(edition_id)