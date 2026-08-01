from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.repository.edition_repository import EditionRepository
from src.repository.competition_repository import CompetitionRepository
from src.repository.team_repository import TeamRepository
from src.schemas.title_schemas import (
    SetEditionChampionsRequest,
    CompetitionChampionsResponse,
    EditionChampionItem,
    TeamTitlesResponse,
    TeamTitleSummary,
    TitleDetailItem
)
from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.comepetition_schemas import CompetitionRead

class TitleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.edition_repo = EditionRepository(session)
        self.comp_repo = CompetitionRepository(session)
        self.team_repo = TeamRepository(session)

    async def set_edition_champions(
        self, 
        edition_id: UUID, 
        payload: SetEditionChampionsRequest
    ):
        """Define os campeões e vices de uma edição (suporta títulos divididos)."""
        edition = await self.edition_repo.get_with_champions(edition_id)
        if not edition:
            raise HTTPException(status_code=404, detail="Edição não encontrada.")

        clean_champion_ids = list(dict.fromkeys(payload.champion_team_ids))
        clean_runner_up_ids = list(dict.fromkeys(payload.runner_up_team_ids or []))

        intersection = set(clean_champion_ids) & set(clean_runner_up_ids)
        if intersection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um mesmo time não pode ser cadastrado como campeão e vice-campeão na mesma edição."
            )


        champions = []
        for team_id in payload.champion_team_ids:
            team = await self.team_repo.get_by_id(team_id)
            if not team:
                raise HTTPException(status_code=404, detail=f"Time campeão ID {team_id} não encontrado.")
            champions.append(team)

        runners_up = []
        if payload.runner_up_team_ids:
            for team_id in payload.runner_up_team_ids:
                team = await self.team_repo.get_by_id(team_id)
                if not team:
                    raise HTTPException(status_code=404, detail=f"Time vice ID {team_id} não encontrado.")
                if team in edition.runners_up:
                    raise HTTPException(status_code=404, datail=f"O time ID {team_id} já é campeão da edição.")
                runners_up.append(team)

        
        edition.champions  = champions
        edition.runners_up = runners_up

        self.session.add(edition)
        await self.session.commit()

        return await self.edition_repo.get_with_champions(edition_id)

    async def get_competition_champions(self, competition_id: UUID) -> CompetitionChampionsResponse:
        """Retorna o histórico de campeões e vices de um campeonato ano a ano."""
        competition = await self.comp_repo.get_by_id(competition_id)
        if not competition:
            raise HTTPException(status_code=404, detail="Competição não encontrada.")

        editions = await self.edition_repo.get_champions_by_competition(competition_id)

        history_items = []
        for ed in editions:
            if ed.champions: # Exibe edições que já possuem campeão definido
                history_items.append(
                    EditionChampionItem(
                        edition_id=ed.id,
                        edition_name=ed.name,
                        year=ed.year,
                        champions=[TeamSimpleResponse.model_validate(c) for c in ed.champions],
                        runners_up=[TeamSimpleResponse.model_validate(r) for r in ed.runners_up]
                    )
                )

        return CompetitionChampionsResponse(
            competition=CompetitionRead.model_validate(competition),
            total_editions=len(history_items),
            history=history_items
        )

    async def get_team_titles(self, team_id: UUID) -> TeamTitlesResponse:
        """Monta a Sala de Troféus do Clube com a contagem total de títulos."""
        team = await self.team_repo.get_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Time não encontrado.")

        editions_won = await self.edition_repo.get_editions_won_by_team(team_id)

        # Agrupa títulos por competição
        grouped_titles: Dict[UUID, Dict] = {}

        for ed in editions_won:
            comp_id = ed.competition.id
            if comp_id not in grouped_titles:
                grouped_titles[comp_id] = {
                    "competition_id": comp_id,
                    "competition_name": ed.competition.name,
                    "competition_type": ed.competition.competition_type.value,
                    "region": ed.competition.region.value,
                    "total_titles": 0,
                    "editions": []
                }

            is_shared = len(ed.champions) > 1
            grouped_titles[comp_id]["editions"].append(
                TitleDetailItem(
                    edition_id=ed.id,
                    edition_name=ed.name,
                    year=ed.year,
                    is_shared=is_shared
                )
            )
            grouped_titles[comp_id]["total_titles"] += 1

        summary_list = [TeamTitleSummary(**item) for item in grouped_titles.values()]
        # Ordena competições pela maior quantidade de troféus
        summary_list.sort(key=lambda x: x.total_titles, reverse=True)

        total_titles_count = sum(item.total_titles for item in summary_list)

        return TeamTitlesResponse(
            team=TeamSimpleResponse.model_validate(team),
            total_titles_count=total_titles_count,
            titles_by_competition=summary_list
        )