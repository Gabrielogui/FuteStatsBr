from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.db.session import get_db
from src.schemas.round_schemas import RoundCreate, RoundResponse
from src.service.round_service import RoundService

router = APIRouter(prefix="/rounds", tags=["Rodadas & Jogos"])

@router.post("/", response_model=RoundResponse, status_code=status.HTTP_201_CREATED)
async def create_round_with_matches(
    payload: RoundCreate,
    db: AsyncSession = Depends(get_db)
):
    """Cadastra uma rodada completa contendo sua lista de jogos."""
    service = RoundService(db)
    return await service.create_round_with_matches(payload)


@router.get("/{round_id}", response_model=RoundResponse)
async def get_round(
    round_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Obtém os detalhes de uma rodada específica e seus jogos."""
    service = RoundService(db)
    return await service.get_round_by_id(round_id)


@router.get("/phase/{phase_id}", response_model=List[RoundResponse])
async def get_rounds_by_phase(
    phase_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Lista todas as rodadas de uma fase do campeonato."""
    service = RoundService(db)
    return await service.get_rounds_by_phase(phase_id)