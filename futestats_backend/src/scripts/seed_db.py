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

async def seed():
    """
    Script para popular o banco de dados com uma edição completa do Brasileirão 2024.
    """
    print("Iniciando seed completo de dados do Brasileirão 2024...")

    async with AsyncSessionLocal() as session:
        try:
            # =========================================================================
            # 1. ESTÁDIOS
            # =========================================================================
            barradao_id = uuid.uuid4()
            fonte_nova_id = uuid.uuid4()
            maracana_id = uuid.uuid4()
            allianz_id = uuid.uuid4()

            barradao = Stadium(
                id=barradao_id,
                name="Estádio Manoel Barradas",
                nickname="Barradão",
                city="Salvador",
                state=StateEnum.BA,
                capacity=35000,
                year=1986,
                address="Avenida Artêmio Valente, Canabrava"
            )

            fonte_nova = Stadium(
                id=fonte_nova_id,
                name="Arena Fonte Nova",
                nickname="Fonte Nova",
                city="Salvador",
                state=StateEnum.BA,
                capacity=48000,
                year=2013,
                address="Ladeira da Fonte das Pedras, Nazaré"
            )

            maracana = Stadium(
                id=maracana_id,
                name="Estádio Jornalista Mário Filho",
                nickname="Maracanã",
                city="Rio de Janeiro",
                state=StateEnum.RJ,
                capacity=78838,
                year=1950,
                address="Avenida Maracanã, Maracanã"
            )

            allianz = Stadium(
                id=allianz_id,
                name="Allianz Parque",
                nickname="Allianz Parque",
                city="São Paulo",
                state=StateEnum.SP,
                capacity=43713,
                year=2014,
                address="Avenida Francisco Matarazzo, Água Branca"
            )

            session.add_all([barradao, fonte_nova, maracana, allianz])
            await session.flush()

            # =========================================================================
            # 2. TIMES
            # =========================================================================
            vitoria_id = uuid.uuid4()
            bahia_id = uuid.uuid4()
            flamengo_id = uuid.uuid4()
            palmeiras_id = uuid.uuid4()

            vitoria = Team(
                id=vitoria_id,
                name="Esporte Clube Vitória",
                short_name="Vitória",
                sigla="VIT",
                city="Salvador",
                state=StateEnum.BA,
                colors=["#000000", "#FF0000"],
                alcunha="Leão da Barra",
                alcunha_color="Rubro-negro",
                year=1899,
                mascot="Leão",
                description="O Leão da Barra, um dos clubes mais tradicionais do futebol nordestino e brasileiro.",
                stadium_id=barradao_id
            )

            bahia = Team(
                id=bahia_id,
                name="Esporte Clube Bahia",
                short_name="Bahia",
                sigla="BAH",
                city="Salvador",
                state=StateEnum.BA,
                colors=["#0000FF", "#FFFFFF", "#FF0000"],
                alcunha="Esquadrão de Aço",
                alcunha_color="Tricolor",
                year=1931,
                mascot="Super-Homem",
                description="Bicampeão Brasileiro e primeiro campeão do futebol brasileiro em 1959.",
                stadium_id=fonte_nova_id
            )

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
                description="Clube de maior torcida do Brasil e detentor de múltiplos títulos nacionais e internacionais.",
                stadium_id=maracana_id
            )

            palmeiras = Team(
                id=palmeiras_id,
                name="Sociedade Esportiva Palmeiras",
                short_name="Palmeiras",
                sigla="PAL",
                city="São Paulo",
                state=StateEnum.SP,
                colors=["#008000", "#FFFFFF"],
                alcunha="Verdão",
                alcunha_color="Alviverde",
                year=1914,
                mascot="Periquito / Porco",
                description="Maior campeão nacional do futebol brasileiro.",
                stadium_id=allianz_id
            )

            session.add_all([vitoria, bahia, flamengo, palmeiras])
            await session.flush()

            # =========================================================================
            # 3. COMPETIÇÃO
            # =========================================================================
            competition_id = uuid.uuid4()
            competition = Competition(
                id=competition_id,
                name="Campeonato Brasileiro Série A",
                competition_type=CompetitionTypeEnum.LEAGUE,
                region=RegionEnum.NACIONAL,
                description="A principal divisão do futebol profissional do Brasil."
            )
            session.add(competition)
            await session.flush()

            # =========================================================================
            # 4. EDIÇÃO 2024
            # =========================================================================
            edition_id = uuid.uuid4()
            edition = Edition(
                id=edition_id,
                name="Campeonato Brasileiro Série A 2024",
                year=2024,
                format=EditionFormatEnum.POINTS,
                competition_id=competition_id,
                relegated_count=4,
                rules_config={
                    "g4_direct_libertadores": 4,
                    "pre_libertadores": 2,
                    "sulamericana": [7, 8, 9, 10, 11, 12],
                    "relegation_zone": [17, 18, 19, 20]
                }
            )
            # Associa os times à edição
            edition.teams = [vitoria, bahia, flamengo, palmeiras]
            session.add(edition)
            await session.flush()

            # =========================================================================
            # 5. FASE DA EDIÇÃO
            # =========================================================================
            phase_id = uuid.uuid4()
            phase = Phase(
                id=phase_id,
                name="Fase Única",
                order=1,
                edition_id=edition_id
            )
            session.add(phase)
            await session.flush()

            # =========================================================================
            # 6. RODADA 1
            # =========================================================================
            round1_id = uuid.uuid4()
            round1 = Round(
                id=round1_id,
                number=1,
                name="1ª Rodada",
                phase_id=phase_id
            )
            session.add(round1)
            await session.flush()

            # Jogos da 1ª Rodada
            match1 = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_id,
                round_id=round1_id,
                home_team_id=vitoria_id,
                away_team_id=palmeiras_id,
                stadium_id=barradao_id,
                date=datetime(2024, 4, 14, 18, 30),
                home_score=2,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )

            match2 = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_id,
                round_id=round1_id,
                home_team_id=flamengo_id,
                away_team_id=bahia_id,
                stadium_id=maracana_id,
                date=datetime(2024, 4, 13, 16, 00),
                home_score=2,
                away_score=1,
                status=MatchStatusEnum.FINISHED
            )
            session.add_all([match1, match2])

            # =========================================================================
            # 7. RODADA 2
            # =========================================================================
            round2_id = uuid.uuid4()
            round2 = Round(
                id=round2_id,
                number=2,
                name="2ª Rodada",
                phase_id=phase_id
            )
            session.add(round2)
            await session.flush()

            # Jogos da 2ª Rodada
            match3 = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_id,
                round_id=round2_id,
                home_team_id=bahia_id,
                away_team_id=vitoria_id,
                stadium_id=fonte_nova_id,
                date=datetime(2024, 4, 21, 16, 00),
                home_score=2,
                away_score=3,
                status=MatchStatusEnum.FINISHED
            )

            match4 = Match(
                id=uuid.uuid4(),
                edition_id=edition_id,
                phase_id=phase_id,
                round_id=round2_id,
                home_team_id=palmeiras_id,
                away_team_id=flamengo_id,
                stadium_id=allianz_id,
                date=datetime(2024, 4, 21, 16, 00),
                home_score=0,
                away_score=0,
                status=MatchStatusEnum.FINISHED
            )
            session.add_all([match3, match4])

            # Commit final das alterações
            await session.commit()
            print("Seed concluído com sucesso!")
            print(f"- Competição: {competition.name}")
            print(f"- Edição: {edition.name}")
            print(f"- Times Cadastrados: {len(edition.teams)}")
            print(f"- Rodadas Inseridas: 2")
            print(f"- Partidas Inseridas: 4")

        except Exception as e:
            print(f"| ERRO | Falha na gravação dos dados: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(seed())