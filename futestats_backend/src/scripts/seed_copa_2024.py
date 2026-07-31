import asyncio
import uuid
from datetime import datetime
from sqlalchemy import select
from src.db.session import AsyncSessionLocal
from src.models import Competition, Edition, Phase, Round, Match, Team, Stadium
from src.models.enums import EditionFormatEnum, MatchStatusEnum

async def seed_copa_2024():
    print(" [4/4] Povoando Copa do Brasil 2024 (Mata-Mata)...")
    async with AsyncSessionLocal() as session:
        try:
            # 1. Busca Competição Pai
            res_comp = await session.execute(
                select(Competition).where(Competition.name == "Copa do Brasil")
            )
            comp = res_comp.scalar_one_or_none()
            if not comp:
                print(" Competição 'Copa do Brasil' não encontrada!")
                return

            # 2. Busca Times
            res_teams = await session.execute(
                select(Team).where(Team.sigla.in_(["FLA", "CAM", "COR", "VAS"]))
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
                    name="Copa do Brasil 2024",
                    year=2024,
                    format=EditionFormatEnum.KNOCKOUT,
                    competition_id=comp.id,
                    relegated_count=None,
                    rules_config={"has_away_goals_rule": False, "penalty_shootout": True},
                )
                '''champion_team_id=team_map["FLA"].id,
                runner_up_team_id=team_map["CAM"].id'''
                edition.teams = teams
                session.add(edition)
                await session.flush()

            # 5. Fases de Mata-Mata (Semifinal e Final)
            res_matches = await session.execute(select(Match).where(Match.edition_id == edition.id))
            if not res_matches.scalars().all():
                # Semifinal
                phase_semi = Phase(id=uuid.uuid4(), name="Semifinal", order=1, edition_id=edition.id)
                session.add(phase_semi)
                await session.flush()

                r_ida_semi = Round(id=uuid.uuid4(), number=1, name="Jogo de Ida", phase_id=phase_semi.id)
                r_volta_semi = Round(id=uuid.uuid4(), number=2, name="Jogo de Volta", phase_id=phase_semi.id)
                session.add_all([r_ida_semi, r_volta_semi])
                await session.flush()

                matches_semi = [
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_semi.id, round_id=r_ida_semi.id,
                        home_team_id=team_map["FLA"].id, away_team_id=team_map["COR"].id,
                        stadium_id=stadium_map["Maracanã"].id, date=datetime(2024, 10, 2, 21, 45),
                        home_score=1, away_score=0, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_semi.id, round_id=r_volta_semi.id,
                        home_team_id=team_map["COR"].id, away_team_id=team_map["FLA"].id,
                        stadium_id=stadium_map["Arena Corinthians"].id, date=datetime(2024, 10, 20, 16, 0),
                        home_score=0, away_score=0, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_semi.id, round_id=r_ida_semi.id,
                        home_team_id=team_map["CAM"].id, away_team_id=team_map["VAS"].id,
                        stadium_id=stadium_map["Arena MRV"].id, date=datetime(2024, 10, 2, 19, 15),
                        home_score=2, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_semi.id, round_id=r_volta_semi.id,
                        home_team_id=team_map["VAS"].id, away_team_id=team_map["CAM"].id,
                        stadium_id=stadium_map["São Januário"].id, date=datetime(2024, 10, 19, 18, 30),
                        home_score=1, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                ]
                session.add_all(matches_semi)

                # Final
                phase_final = Phase(id=uuid.uuid4(), name="Final", order=2, edition_id=edition.id)
                session.add(phase_final)
                await session.flush()

                r_ida_final = Round(id=uuid.uuid4(), number=1, name="Jogo de Ida", phase_id=phase_final.id)
                r_volta_final = Round(id=uuid.uuid4(), number=2, name="Jogo de Volta", phase_id=phase_final.id)
                session.add_all([r_ida_final, r_volta_final])
                await session.flush()

                matches_final = [
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_final.id, round_id=r_ida_final.id,
                        home_team_id=team_map["FLA"].id, away_team_id=team_map["CAM"].id,
                        stadium_id=stadium_map["Maracanã"].id, date=datetime(2024, 11, 3, 16, 0),
                        home_score=3, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                    Match(
                        id=uuid.uuid4(), edition_id=edition.id, phase_id=phase_final.id, round_id=r_volta_final.id,
                        home_team_id=team_map["CAM"].id, away_team_id=team_map["FLA"].id,
                        stadium_id=stadium_map["Arena MRV"].id, date=datetime(2024, 11, 10, 16, 0),
                        home_score=0, away_score=1, status=MatchStatusEnum.FINISHED
                    ),
                ]
                session.add_all(matches_final)

            await session.commit()
            print(" Copa do Brasil 2024 sincronizada com sucesso!")
        except Exception as e:
            print(f"| ERRO | Falha no seed da Copa 2024: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_copa_2024())