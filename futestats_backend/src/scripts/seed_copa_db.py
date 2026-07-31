# src/scripts/seed_copa_db.py

import asyncio
import uuid
from datetime import datetime
from src.db.session import AsyncSessionLocal
from src.models import (
    Stadium,
    Team,
    Competition,
    Edition,
    Phase,
    Round,
    Match
)
from src.models.enums import (
    StateEnum,
    CompetitionTypeEnum,
    RegionEnum,
    EditionFormatEnum,
    MatchStatusEnum
)

async def seed_copa():
    """
    Script para popular o banco com uma edição completa de Mata-Mata (Copa do Brasil 2024).
    Contém Semifinais e Final com jogos de ida e volta.
    """
    print("Iniciando seed de dados da Copa do Brasil 2024 (Mata-Mata)...")

    async with AsyncSessionLocal() as session:
        try:
            # =========================================================================
            # 1. ESTÁDIOS
            # =========================================================================
            maracana_id = uuid.uuid4()
            arena_mrv_id = uuid.uuid4()
            neo_quimica_id = uuid.uuid4()
            sao_januario_id = uuid.uuid4()

            maracana = Stadium(
                id=maracana_id,
                name="Estádio Jornalista Mário Filho",
                nickname="Maracanã",
                city="Rio de Janeiro",
                state=StateEnum.RJ,
                capacity=78838,
                year=1950,
                address="Avenida Maracanã"
            )

            arena_mrv = Stadium(
                id=arena_mrv_id,
                name="Arena MRV",
                nickname="Arena MRV",
                city="Belo Horizonte",
                state=StateEnum.MG,
                capacity=46000,
                year=2023,
                address="Rua Cristina Maria de Assis, Califórnia"
            )

            neo_quimica = Stadium(
                id=neo_quimica_id,
                name="Neo Química Arena",
                nickname="Arena Corinthians",
                city="São Paulo",
                state=StateEnum.SP,
                capacity=49000,
                year=2014,
                address="Avenida Miguel Ignácio Curi, Itaquera"
            )

            sao_januario = Stadium(
                id=sao_januario_id,
                name="Estádio de São Januário",
                nickname="São Januário",
                city="Rio de Janeiro",
                state=StateEnum.RJ,
                capacity=21880,
                year=1927,
                address="Rua General Almério de Moura, Vasco da Gama"
            )

            session.add_all([maracana, arena_mrv, neo_quimica, sao_januario])
            await session.flush()

            # =========================================================================
            # 2. TIMES
            # =========================================================================
            flamengo_id = uuid.uuid4()
            atletico_mg_id = uuid.uuid4()
            corinthians_id = uuid.uuid4()
            vasco_id = uuid.uuid4()

            flamengo = Team(
                id=flamengo_id,
                name="Clube de Regatas do Flamengo",
                short_name="Flamengo",
                sigla="FLA",
                city="Rio de Janeiro",
                state=StateEnum.RJ,
                colors=["#FF0000", "#000000"],
                alcunha="Mengão",
                alcunha_color="Rubro-negro",
                year=1895,
                mascot="Urubu",
                stadium_id=maracana_id
            )

            atletico_mg = Team(
                id=atletico_mg_id,
                name="Clube Atlético Mineiro",
                short_name="Atlético-MG",
                sigla="CAM",
                city="Belo Horizonte",
                state=StateEnum.MG,
                colors=["#000000", "#FFFFFF"],
                alcunha="Galo",
                alcunha_color="Alvinegro",
                year=1908,
                mascot="Galo",
                stadium_id=arena_mrv_id
            )

            corinthians = Team(
                id=corinthians_id,
                name="Sport Club Corinthians Paulista",
                short_name="Corinthians",
                sigla="COR",
                city="São Paulo",
                state=StateEnum.SP,
                colors=["#FFFFFF", "#000000"],
                alcunha="Timão",
                alcunha_color="Alvinegro",
                year=1910,
                mascot="Mosqueteiro",
                stadium_id=neo_quimica_id
            )

            vasco = Team(
                id=vasco_id,
                name="Club de Regatas Vasco da Gama",
                short_name="Vasco",
                sigla="VAS",
                city="Rio de Janeiro",
                state=StateEnum.RJ,
                colors=["#000000", "#FFFFFF"],
                alcunha="Gigante da Colina",
                alcunha_color="Cruzmaltino",
                year=1898,
                mascot="Almirante",
                stadium_id=sao_januario_id
            )

            session.add_all([flamengo, atletico_mg, corinthians, vasco])
            await session.flush()

            # =========================================================================
            # 3. COMPETIÇÃO DE COPA
            # =========================================================================
            copa_id = uuid.uuid4()
            copa_br = Competition(
                id=copa_id,
                name="Copa do Brasil",
                competition_type=CompetitionTypeEnum.CUP,
                region=RegionEnum.NACIONAL,
                description="O torneio mais democrático do futebol brasileiro."
            )
            session.add(copa_br)
            await session.flush()

            # =========================================================================
            # 4. EDIÇÃO 2024
            # =========================================================================
            edition_id = uuid.uuid4()
            edition = Edition(
                id=edition_id,
                name="Copa do Brasil 2024",
                year=2024,
                format=EditionFormatEnum.KNOCKOUT,
                competition_id=copa_id,
                relegated_count=None,
                rules_config={
                    "has_away_goals_rule": False,
                    "penalty_shootout": True
                },
                champion_team_id=flamengo_id,
                runner_up_team_id=atletico_mg_id
            )
            edition.teams = [flamengo, atletico_mg, corinthians, vasco]
            session.add(edition)
            await session.flush()

            # =========================================================================
            # 5. FASE 1: SEMIFINAL
            # =========================================================================
            phase_semi_id = uuid.uuid4()
            phase_semi = Phase(
                id=phase_semi_id,
                name="Semifinal",
                order=1,
                edition_id=edition_id
            )
            session.add(phase_semi)
            await session.flush()

            # Rodadas (Ida e Volta)
            r_ida_semi = Round(id=uuid.uuid4(), number=1, name="Jogo de Ida", phase_id=phase_semi_id)
            r_volta_semi = Round(id=uuid.uuid4(), number=2, name="Jogo de Volta", phase_id=phase_semi_id)
            session.add_all([r_ida_semi, r_volta_semi])
            await session.flush()

            # Duelo 1: Flamengo x Corinthians
            match_semi1_ida = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_semi_id,
                round_id=r_ida_semi.id,
                home_team_id=flamengo_id,
                away_team_id=corinthians_id,
                stadium_id=maracana_id,
                date=datetime(2024, 10, 2, 21, 45),
                home_score=1,
                away_score=0,
                status=MatchStatusEnum.FINISHED
            )

            match_semi1_volta = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_semi_id,
                round_id=r_volta_semi.id,
                home_team_id=corinthians_id,
                away_team_id=flamengo_id,
                stadium_id=neo_quimica_id,
                date=datetime(2024, 10, 20, 16, 0),
                home_score=0,
                away_score=0,
                status=MatchStatusEnum.FINISHED
            )

            # Duelo 2: Atlético-MG x Vasco
            match_semi2_ida = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_semi_id,
                round_id=r_ida_semi.id,
                home_team_id=atletico_mg_id,
                away_team_id=vasco_id,
                stadium_id=arena_mrv_id,
                date=datetime(2024, 10, 2, 19, 15),
                home_score=2,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )

            match_semi2_volta = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_semi_id,
                round_id=r_volta_semi.id,
                home_team_id=vasco_id,
                away_team_id=atletico_mg_id,
                stadium_id=sao_januario_id,
                date=datetime(2024, 10, 19, 18, 30),
                home_score=1,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )

            session.add_all([match_semi1_ida, match_semi1_volta, match_semi2_ida, match_semi2_volta])

            # =========================================================================
            # 6. FASE 2: GRANDE FINAL
            # =========================================================================
            phase_final_id = uuid.uuid4()
            phase_final = Phase(
                id=phase_final_id,
                name="Final",
                order=2,
                edition_id=edition_id
            )
            session.add(phase_final)
            await session.flush()

            r_ida_final = Round(id=uuid.uuid4(), number=1, name="Jogo de Ida", phase_id=phase_final_id)
            r_volta_final = Round(id=uuid.uuid4(), number=2, name="Jogo de Volta", phase_id=phase_final_id)
            session.add_all([r_ida_final, r_volta_final])
            await session.flush()

            # Jogo de Ida da Final: Flamengo 3 x 1 Atlético-MG
            match_final_ida = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_final_id,
                round_id=r_ida_final.id,
                home_team_id=flamengo_id,
                away_team_id=atletico_mg_id,
                stadium_id=maracana_id,
                date=datetime(2024, 11, 3, 16, 0),
                home_score=3,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )

            # Jogo de Volta da Final: Atlético-MG 0 x 1 Flamengo
            match_final_volta = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_final_id,
                round_id=r_volta_final.id,
                home_team_id=atletico_mg_id,
                away_team_id=flamengo_id,
                stadium_id=arena_mrv_id,
                date=datetime(2024, 11, 10, 16, 0),
                home_score=0,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )

            session.add_all([match_final_ida, match_final_volta])

            # Commit final das inserções
            await session.commit()
            print("Seed da Copa do Brasil 2024 concluído com sucesso!")
            print(f"- Edição: {edition.name}")
            print(f"- Fases: Semifinal e Final")
            print(f"- Total de Partidas do Mata-Mata: 6")

        except Exception as e:
            print(f"| ERRO | Falha na gravação do seed da Copa: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(seed_copa())