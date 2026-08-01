from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.db.session import get_db
from src.models.enums import CompetitionTypeEnum

from src.schemas.comepetition_schemas import CompetitionCreate, CompetitionRead
from src.schemas.photo_schemas import PhotoRead
from src.schemas.title_schemas import CompetitionChampionsResponse, CompetitionTopWinnersResponse

from src.service.competition_service import CompetitionService
from src.service.title_service import TitleService

router = APIRouter(prefix="/competitions", tags=["Competições"])

@router.post("/", response_model=CompetitionRead, status_code=status.HTTP_201_CREATED)
async def create_competition(
    payload: CompetitionCreate,
    db: AsyncSession = Depends(get_db)
):
    service = CompetitionService(db)
    return await service.create_competition(payload)

@router.get("/", response_model=List[CompetitionRead])
async def list_competitions(
    db: AsyncSession = Depends(get_db)
):
    service = CompetitionService(db)
    return await service.get_all()

@router.get("/{comp_id}", response_model=CompetitionRead)
async def get_competition(
    comp_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = CompetitionService(db)
    return await service.get_by_id(comp_id)

@router.get("/type/{comp_type}", response_model=List[CompetitionRead])
async def get_competitions_by_type(
    comp_type: CompetitionTypeEnum,
    db: AsyncSession = Depends(get_db)
):
    service = CompetitionService(db)
    return await service.get_by_type(comp_type)

@router.get("/{competition_id}/champions", response_model=CompetitionChampionsResponse, tags=["Competições", "Títulos"])
async def get_competition_champions(
    competition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retorna a galeria histórica de campeões e vices de uma competição ano a ano."""
    service = TitleService(db)
    return await service.get_competition_champions(competition_id)

@router.get("/{competition_id}/top-winners", response_model=CompetitionTopWinnersResponse, tags=["Competições", "Títulos"])
async def get_competition_top_winners(
    competition_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retorna o ranking dos clubes com mais títulos na história da competição."""
    service = TitleService(db)
    return await service.get_competition_top_winners(competition_id)

@router.post("/{comp_id}/logo", response_model=PhotoRead, status_code=status.HTTP_201_CREATED)
async def upload_competition_logo(
    comp_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Rota para upload do logo/escudo oficial da competição."""
    service = CompetitionService(db)
    return await service.upload_logo(comp_id, file)