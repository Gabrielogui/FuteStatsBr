# src/scripts/05_seed_hybrid_2024.py

import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from src.db.session import AsyncSessionLocal
from src.models import Competition, Edition, Phase, Round, Match, Team, Stadium
from src.models.enums import (
    CompetitionTypeEnum, 
    RegionEnum, 
    EditionFormatEnum, 
    MatchStatusEnum
)
from src.scripts.utils import get_or_create

async def seed_hybrid_2024():
    print(" [5/5] Povoando Torneio Híbrido (Campeonato Baiano 2024)...")
    async with AsyncSessionLocal() as session:
        try:
            # =========================================================================
            # 1. BUSCA DE TIMES E ESTÁDIOS JÁ EXISTENTES
            # =========================================================================
            res_teams = await session.execute(
                select(Team).where(Team.sigla.in_(["VIT", "BAH", "FLA", "PAL"]))
            )
            teams = list(res_teams.scalars().all())
            team_map = {t.sigla: t for t in teams}

            if not team_map:
                print(" | ERRO | Nenhum time encontrado. Execute '01_seed_stadiums_and_teams.py' primeiro.")
                return

            res_stadiums = await session.execute(select(Stadium))
            stadiums = list(res_stadiums.scalars().all())
            stadium_map = {s.nickname: s for s in stadiums}

            # =========================================================================
            # 2. COMPETIÇÃO PAI (ESTADUAL)
            # =========================================================================
            comp_filter = {"name": "Campeonato Baiano"}
            comp_data = {
                "id": uuid.uuid4(),
                "name": "Campeonato Baiano",
                "competition_type": CompetitionTypeEnum.STATE,
                "region": RegionEnum.NORDESTE,
                "description": "O principal campeonato estadual da Bahia."
            }
            comp = await get_or_create(session, Competition, comp_filter, comp_data)

            # =========================================================================
            # 3. EDIÇÃO HÍBRIDA 2024
            # =========================================================================
            res_ed = await session.execute(
                select(Edition).where(Edition.competition_id == comp.id, Edition.year == 2024)
            )
            edition = res_ed.scalar_one_or_none()

            if not edition:
                edition = Edition(
                    id=uuid.uuid4(),
                    name="Campeonato Baiano 2024",
                    year=2024,
                    format=EditionFormatEnum.HYBRID, # <--- FORMATO HÍBRIDO
                    competition_id=comp.id,
                    relegated_count=2,
                    rules_config={
                        "qualified_next_stage": 2, # Os 2 primeiros vão para a Final
                        "has_knockout": True
                    }
                )
                edition.teams = teams
                session.add(edition)
                await session.flush()

            # =========================================================================
            # 4. FASE 1: FASE DE GRUPOS (PONTOS CORRIDOS)
            # =========================================================================
            res_matches = await session.execute(
                select(Match).where(Match.edition_id == edition.id)
            )
            if not res_matches.scalars().all():
                phase1 = Phase(
                    id=uuid.uuid4(),
                    name="Fase de Grupos",
                    order=1,
                    edition_id=edition.id
                )
                session.add(phase1)
                await session.flush()

                r1 = Round(id=uuid.uuid4(), number=1, name="1ª Rodada", phase_id=phase1.id)
                r2 = Round(id=uuid.uuid4(), number=2, name="2ª Rodada", phase_id=phase1.id)
                session.add_all([r1, r2])
                await session.flush()

                # Jogos da Fase de Grupos
                matches_phase1 = [
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase1.id, round_id=r1.id,
                        home_team_id=team_map["VIT"].id, away_team_id=team_map["BAH"].id,
                        stadium_id=stadium_map["Barradão"].id, date=datetime(2024, 2, 18, 16, 0),
                        home_score=3, away_score=2, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase1.id, round_id=r1.id,
                        home_team_id=team_map["FLA"].id, away_team_id=team_map["PAL"].id,
                        stadium_id=stadium_map["Maracanã"].id, date=datetime(2024, 2, 18, 18, 30),
                        home_score=1, away_score=0, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase1.id, round_id=r2.id,
                        home_team_id=team_map["BAH"].id, away_team_id=team_map["FLA"].id,
                        stadium_id=stadium_map["Fonte Nova"].id, date=datetime(2024, 2, 25, 16, 0),
                        home_score=2, away_score=0, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase1.id, round_id=r2.id,
                        home_team_id=team_map["PAL"].id, away_team_id=team_map["VIT"].id,
                        stadium_id=stadium_map["Allianz Parque"].id, date=datetime(2024, 2, 25, 16, 0),
                        home_score=1, away_score=2, status=MatchStatusEnum.FINISHED
                    ),
                ]
                session.add_all(matches_phase1)

                # =========================================================================
                # 5. FASE 2: GRANDE FINAL (MATA-MATA DE IDA E VOLTA)
                # =========================================================================
                phase2 = Phase(
                    id=uuid.uuid4(),
                    name="Final",
                    order=2,
                    edition_id=edition.id
                )
                session.add(phase2)
                await session.flush()

                r_ida = Round(id=uuid.uuid4(), number=1, name="Jogo de Ida", phase_id=phase2.id)
                r_volta = Round(id=uuid.uuid4(), number=2, name="Jogo de Volta", phase_id=phase2.id)
                session.add_all([r_ida, r_volta])
                await session.flush()

                matches_phase2 = [
                    # Jogo de Ida da Final: Vitória 3 x 2 Bahia (Barradão)
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase2.id, round_id=r_ida.id,
                        home_team_id=team_map["VIT"].id, away_team_id=team_map["BAH"].id,
                        stadium_id=stadium_map["Barradão"].id, date=datetime(2024, 3, 31, 16, 0),
                        home_score=3, away_score=2, status=MatchStatusEnum.FINISHED
                    ),
                    # Jogo de Volta da Final: Bahia 1 x 1 Vitória (Fonte Nova)
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase2.id, round_id=r_volta.id,
                        home_team_id=team_map["BAH"].id, away_team_id=team_map["VIT"].id,
                        stadium_id=stadium_map["Fonte Nova"].id, date=datetime(2024, 4, 7, 16, 0),
                        home_score=1, away_score=1, status=MatchStatusEnum.FINISHED
                    )
                ]
                session.add_all(matches_phase2)

                # Define o Vitória como Campeão Baiano 2024 (4x3 no agregado)
                '''edition.champion_team_id = team_map["VIT"].id
                edition.runner_up_team_id = team_map["BAH"].id'''

            await session.commit()
            print(" Campeonato Baiano 2024 (Híbrido) sincronizado com sucesso!")

        except Exception as e:
            print(f"| ERRO | Falha no seed do Torneio Híbrido: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_hybrid_2024())