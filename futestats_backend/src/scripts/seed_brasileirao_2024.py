import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.session import AsyncSessionLocal
from src.models import Competition, Edition, Phase, Round, Match, Team, Stadium
from src.models.enums import EditionFormatEnum, MatchStatusEnum

async def seed_brasileirao_2024():
    print(" [3/4] Povoando Brasileirão 2024 (Pontos Corridos)...")
    async with AsyncSessionLocal() as session:
        try:
            # 1. Busca Competição Pai
            res_comp = await session.execute(
                select(Competition).where(Competition.name == "Campeonato Brasileiro Série A")
            )
            comp = res_comp.scalar_one_or_none()
            if not comp:
                print(" Competição 'Campeonato Brasileiro Série A' não encontrada!")
                return

            # 2. Busca Times
            res_teams = await session.execute(
                select(Team).where(Team.sigla.in_(["VIT", "PAL", "FLA", "BAH"]))
            )
            teams = list(res_teams.scalars().all())
            team_map = {t.sigla: t for t in teams}

            # 3. Busca Estádios
            res_stadiums = await session.execute(select(Stadium))
            stadiums = list(res_stadiums.scalars().all())
            stadium_map = {s.nickname: s for s in stadiums}

            # 4. Verifica/Cria Edição 2024
            res_ed = await session.execute(
                select(Edition).where(Edition.competition_id == comp.id, Edition.year == 2024)
            )
            edition = res_ed.scalar_one_or_none()

            if not edition:
                edition = Edition(
                    id=uuid.uuid4(),
                    name="Campeonato Brasileiro Série A 2024",
                    year=2024,
                    format=EditionFormatEnum.POINTS,
                    competition_id=comp.id,
                    relegated_count=4,
                    rules_config={
                        "g4_direct_libertadores": 4,
                        "pre_libertadores": 2,
                        "sulamericana": [7, 8, 9, 10, 11, 12]
                    }
                )
                edition.teams = teams
                session.add(edition)
                await session.flush()

            # 5. Verifica/Cria Fase
            res_phase = await session.execute(
                select(Phase).where(Phase.edition_id == edition.id, Phase.name == "Fase Única")
            )
            phase = res_phase.scalar_one_or_none()
            if not phase:
                phase = Phase(id=uuid.uuid4(), name="Fase Única", order=1, edition_id=edition.id)
                session.add(phase)
                await session.flush()

            # 6. Rodadas e Jogos (Se não existirem)
            res_matches = await session.execute(select(Match).where(Match.edition_id == edition.id))
            if not res_matches.scalars().all():
                round1 = Round(id=uuid.uuid4(), number=1, name="1ª Rodada", phase_id=phase.id)
                round2 = Round(id=uuid.uuid4(), number=2, name="2ª Rodada", phase_id=phase.id)
                session.add_all([round1, round2])
                await session.flush()

                matches = [
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase.id, round_id=round1.id,
                        home_team_id=team_map["VIT"].id, away_team_id=team_map["PAL"].id,
                        stadium_id=stadium_map["Barradão"].id, date=datetime(2024, 4, 14, 18, 30),
                        home_score=2, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase.id, round_id=round1.id,
                        home_team_id=team_map["FLA"].id, away_team_id=team_map["BAH"].id,
                        stadium_id=stadium_map["Maracanã"].id, date=datetime(2024, 4, 13, 16, 0),
                        home_score=2, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase.id, round_id=round2.id,
                        home_team_id=team_map["BAH"].id, away_team_id=team_map["VIT"].id,
                        stadium_id=stadium_map["Fonte Nova"].id, date=datetime(2024, 4, 21, 16, 0),
                        home_score=2, away_score=3, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase.id, round_id=round2.id,
                        home_team_id=team_map["PAL"].id, away_team_id=team_map["FLA"].id,
                        stadium_id=stadium_map["Allianz Parque"].id, date=datetime(2024, 4, 21, 16, 0),
                        home_score=0, away_score=0, status=MatchStatusEnum.FINISHED
                    ),
                ]
                session.add_all(matches)

            await session.commit()
            print(" Brasileirão 2024 sincronizado com sucesso!")
        except Exception as e:
            print(f"| ERRO | Falha no seed do Brasileirão 2024: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_brasileirao_2024())