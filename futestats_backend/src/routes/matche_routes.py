from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from uuid import UUID

from src.db.session import get_db
from src.schemas.h2h_schemas import H2HSummaryResponse
from src.service.h2h_service import H2HService

router = APIRouter(prefix="/matches", tags=["Partidas & Confrontos (H2H)"])

@router.get("/head-to-head", response_model=H2HSummaryResponse)
async def get_head_to_head_summary(
    team1_id         : UUID = Query(..., description="ID do primeiro time"),
    team2_id         : UUID = Query(..., description="ID do segundo time"),
    competition_id   : Optional[UUID] = Query(None, description="Filtrar por uma competição específica"),
    stadium_id       : Optional[UUID] = Query(None, description="Filtrar por um estádio específico"),
    only_home_team_id: Optional[UUID] = Query(None, description="Filtrar apenas jogos onde este time foi o mandante"),
    start_date       : Optional[datetime] = Query(None, description="Data inicial do filtro"),
    end_date         : Optional[datetime] = Query(None, description="Data final do filtro"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna o histórico estatístico de confronto direto (H2H) entre dois clubes com filtros dinâmicos.
    """
    service = H2HService(db)
    return await service.get_head_to_head_summary(
        team1_id=team1_id,
        team2_id=team2_id,
        competition_id=competition_id,
        stadium_id=stadium_id,
        only_home_team_id=only_home_team_id,
        start_date=start_date,
        end_date=end_date
    )