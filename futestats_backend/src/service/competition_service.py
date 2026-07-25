from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Request, UploadFile, status
import uuid

from src.models.competition_model import Competition
from src.models.enums import CompetitionTypeEnum, EntityTypesEnum
from src.repository.competition_repository import CompetitionRepository
from src.schemas.comepetition_schemas import CompetitionCreate, CompetitionUpdate
from src.service.image_service import ImageService

class CompetitionService:
    def __init__(self, session: AsyncSession):
        self.session                = session
        self.competition_repository = CompetitionRepository(session)
        self.image_service          = ImageService(session)

    async def create_competition(self, competition_schema: CompetitionCreate) -> Competition:
        return await self.competition_repository.create(competition_schema)

    async def get_by_id(self, comp_id: uuid.UUID) -> Competition:
        competition = await self.competition_repository.get_by_id(comp_id)
        if not competition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competição não encontrada."
            )
        return competition

    async def get_all(self) -> Sequence[Competition]:
        return await self.competition_repository.get_all()

    async def get_by_type(self, comp_type: CompetitionTypeEnum) -> Sequence[Competition]:
        return await self.competition_repository.get_by_type(comp_type)

    async def upload_logo(self, comp_id: uuid.UUID, file: UploadFile, request: Request):
        # Valida existência da competição
        await self.get_by_id(comp_id)
        
        # Salva a foto associando ao tipo COMPETITION
        return await self.image_service.upload_entity_images(
            file=file,
            entity_type=EntityTypesEnum.COMPETITION,
            entity_id=comp_id
        )

# TODO: COMENTAR FUNÇÕES