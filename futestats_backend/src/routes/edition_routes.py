from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.db.session import get_db

from src.schemas.edition_schemas import EditionCreate, EditionResponse, EditionTeamsUpdate
from src.schemas.standings_schemas import StandingsTableResponse
from src.schemas.bracket_schemas import BracketResponse
from src.schemas.title_schemas import SetEditionChampionsRequest

from src.service.bracket_service import BracketService
from src.service.edition_service import EditionService
from src.service.standing_service import StandingsService
from src.service.title_service import TitleService



router = APIRouter(prefix="/editions", tags=["Edições (Anos dos Campeonatos)"])

@router.post("/", response_model=EditionResponse, status_code=status.HTTP_201_CREATED)
async def create_edition(
    payload: EditionCreate,
    db: AsyncSession = Depends(get_db)
):
    service = EditionService(db)
    return await service.create_edition(payload)

@router.get("/{edition_id}", response_model=EditionResponse)
async def get_edition(
    edition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = EditionService(db)
    return await service.get_by_id(edition_id)

@router.get("/competition/{competition_id}", response_model=List[EditionResponse])
async def get_editions_by_competition(
    competition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = EditionService(db)
    return await service.get_by_competition(competition_id)

@router.get("/{edition_id}/table", response_model=StandingsTableResponse)
async def get_edition_table(
    edition_id: UUID,
    start_round: Optional[int] = None,
    until_round: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Calcula a tabela de classificação oficial da edição (com suporte a filtro de rodada)."""
    service = StandingsService(db)
    return await service.calculate_edition_standings(edition_id, start_round, until_round)

@router.get("/{edition_id}/bracket", response_model=BracketResponse)
async def get_edition_bracket(
    edition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retorna a árvore de mata-mata completa da edição de Copa (Oitavas -> Quartas -> Semi -> Final)."""
    service = BracketService(db)
    return await service.get_edition_bracket(edition_id)

@router.put("/{edition_id}/champions", status_code=status.HTTP_200_OK, tags=["Edições (Anos dos Campeonatos)", "Títulos"])
async def set_edition_champions(
    edition_id: UUID,
    payload: SetEditionChampionsRequest,
    db: AsyncSession = Depends(get_db)
):
    """Define ou atualiza os campeões e vices de uma edição (suporta títulos divididos)."""
    service = TitleService(db)
    return await service.set_edition_champions(edition_id, payload)

@router.post("/{edition_id}/teams", response_model=EditionResponse)
async def add_teams_to_edition(
    edition_id: UUID,
    payload: EditionTeamsUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Associa uma lista de times à edição informada."""
    service = EditionService(db)
    return await service.add_teams_to_edition(edition_id, payload.team_ids)