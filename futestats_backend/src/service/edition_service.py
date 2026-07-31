from typing import Sequence, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.models.edition_model import Edition
from src.repository.edition_repository import EditionRepository
from src.repository.competition_repository import CompetitionRepository
from src.repository.team_repository import TeamRepository
from src.schemas.edition_schemas import EditionCreate, EditionUpdate

class EditionService:
    def __init__(self, session: AsyncSession):
        self.session      = session
        self.edition_repo = EditionRepository(session)
        self.comp_repo    = CompetitionRepository(session)
        self.team_repo    = TeamRepository(session)

    async def create_edition(self, edition_schema: EditionCreate) -> Edition:
        # Verifica se a competição pai existe
        competition = await self.comp_repo.get_by_id(edition_schema.competition_id)
        if not competition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competição informada não existe."
            )

        async with self.session.begin():
            new_edition = Edition(
                name=edition_schema.name,
                year=edition_schema.year,
                format=edition_schema.format,
                competition_id=edition_schema.competition_id,
                relegated_count=edition_schema.relegated_count,
                rules_config=edition_schema.rules_config
            )
            self.session.add(new_edition)
            await self.session.flush()

            # Associa os times passados na criação
            if edition_schema.team_ids:
                teams = []
                for team_id in edition_schema.team_ids:
                    team = await self.team_repo.get_by_id(team_id)
                    if team:
                        teams.append(team)
                new_edition.teams = teams

        return await self.edition_repo.get_with_relations(new_edition.id)

    async def get_by_id(self, edition_id: UUID) -> Edition:
        edition = await self.edition_repo.get_with_relations(edition_id)
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Edição não encontrada."
            )
        return edition

    # TODO: CONFERIR SE A COMPETIÇÃO ESTÁ CADASTRADA
    async def get_by_competition(self, competition_id: UUID) -> Sequence[Edition]:
        return await self.edition_repo.get_by_competition(competition_id)

    async def add_teams_to_edition(self, edition_id: UUID, team_ids: List[UUID]) -> Edition:
        """Adiciona/atualiza a lista de clubes participantes da edição."""
        edition = await self.edition_repo.get_with_relations(edition_id)
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Edição não encontrada."
            )

        async with self.session.begin():
            for team_id in team_ids:
                team = await self.team_repo.get_by_id(team_id)
                if team and team not in edition.teams:
                    edition.teams.append(team)
            self.session.add(edition)

        return await self.edition_repo.get_with_relations(edition_id)