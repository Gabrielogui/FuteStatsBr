from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

from src.models.edition_model import Round
from src.models.match_model import Match
from src.models.enums import EditionFormatEnum

from src.schemas.round_schemas import RoundCreate

from src.repository.round_repository import RoundRepository
from src.repository.edition_repository import EditionRepository

class RoundService:
    def __init__(self, session: AsyncSession):
        self.session            = session
        self.round_repository   = RoundRepository(session)
        self.edition_repository = EditionRepository(session)

    async def create_round_with_matches(self, round_schema: RoundCreate) -> Round:
        """
        Cadastra a rodada e todos os seus jogos em uma única transação.
        Vincula automaticamente edition_id e phase_id aos jogos.
        """
        edition = await self.edition_repository.get_by_id(round.edition_id)
        if not edition:
            raise HTTPException(status_code=404, detail="Edição informada não existe.")

        round_name = round_schema.name

        if not round_schema.name:
            if edition.format == EditionFormatEnum.POINTS:
                round_name = f"{round_schema.number}ª Rodada"
            elif edition.format == EditionFormatEnum.KNOCKOUT:
                round_name = "Jogo de Ida" if round_schema.number == 1 else ("Jogo de Volta" if round_schema.number == 2 else f"{round_schema.number}º Jogo")
            else:
                round_name = f"{round_schema.number}ª Rodada"


        async with self.session.begin():
            # 1. Instancia a Rodada
            new_round = Round(
                number=round_schema.number,
                name=round_name,
                phase_id=round_schema.phase_id
            )
            self.session.add(new_round)
            await self.session.flush() 

            # 2. Instancia cada Jogo vinculado à Edição, Fase e à Rodada
            for match_data in round_schema.matches:
                if match_data.home_team_id == match_data.away_team_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="O time mandante e visitante não podem ser iguais."
                    )

                new_match = Match(
                    edition_id=round_schema.edition_id,
                    phase_id=round_schema.phase_id,
                    round_id=new_round.id,
                    home_team_id=match_data.home_team_id,
                    away_team_id=match_data.away_team_id,
                    stadium_id=match_data.stadium_id,
                    date=match_data.date,
                    home_score=match_data.home_score,
                    away_score=match_data.away_score,
                    status=match_data.status
                )
                self.session.add(new_match)

        return await self.round_repository.get_with_matches(new_round.id)

    async def get_round_by_id(self, round_id: UUID) -> Round:
        round_obj = await self.round_repository.get_with_matches(round_id)
        if not round_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rodada não encontrada."
            )
        return round_obj

    async def get_rounds_by_phase(self, phase_id: UUID) -> List[Round]:
        return await self.round_repository.get_by_phase(phase_id)