from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import uuid

from src.models.edition_model import Phase
from src.repository.phase_repository import PhaseRepository
from src.repository.edition_repository import EditionRepository
from src.schemas.phase_schemas import PhaseCreate

class PhaseService:
    def __init__(self, session: AsyncSession):
        self.session          = session
        self.phase_repository = PhaseRepository(session)
        self.edition_repo     = EditionRepository(session)

    async def create_phase(self, phase_schema: PhaseCreate) -> Phase:
        # Garante que a edição existe antes de criar a fase
        edition = await self.edition_repo.get_by_id(phase_schema.edition_id)
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Edição informada não existe."
            )
        return await self.phase_repository.create(phase_schema)

    async def get_by_id(self, phase_id: uuid.UUID) -> Phase:
        phase = await self.phase_repository.get_by_id(phase_id)
        if not phase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fase não encontrada."
            )
        return phase

    async def get_by_edition(self, edition_id: uuid.UUID) -> Sequence[Phase]:
        return await self.phase_repository.get_by_edition(edition_id)