from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.db.session import get_db

from src.schemas.phase_schemas import PhaseCreate, PhaseResponse
from src.schemas.standings_schemas import StandingsTableResponse
from src.schemas.bracket_schemas import KnockoutPhaseResponse

from src.service.phase_service import PhaseService
from src.service.standing_service import StandingsService
from src.service.bracket_service import BracketService



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

@router.get("/{phase_id}/table", response_model=StandingsTableResponse)
async def get_phase_table(phase_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retorna a tabela de classificação de uma fase específica (ex: Fase de Grupos)."""
    service = StandingsService(db)
    return await service.calculate_phase_standings(phase_id)

@router.get("/{phase_id}/bracket", response_model=KnockoutPhaseResponse)
async def get_phase_bracket(
    phase_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retorna os confrontos e placares agregados de uma fase eliminatória específica."""
    service = BracketService(db)
    return await service.get_phase_bracket(phase_id)