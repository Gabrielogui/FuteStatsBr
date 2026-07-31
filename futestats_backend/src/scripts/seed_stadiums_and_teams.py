import asyncio
import uuid
from src.db.session import AsyncSessionLocal
from src.models import Stadium, Team
from src.models.enums import StateEnum
from src.scripts.utils import get_or_create

STADIUMS_DATA = [
    {
        "filter": {"name": "Estádio Manoel Barradas"},
        "data": {
            "nickname": "Barradão",
            "city": "Salvador",
            "state": StateEnum.BA,
            "capacity": 35000,
            "year": 1986,
            "address": "Avenida Artêmio Valente, Canabrava"
        }
    },
    {
        "filter": {"name": "Arena Fonte Nova"},
        "data": {
            "nickname": "Fonte Nova",
            "city": "Salvador",
            "state": StateEnum.BA,
            "capacity": 48000,
            "year": 2013,
            "address": "Ladeira da Fonte das Pedras, Nazaré"
        }
    },
    {
        "filter": {"name": "Estádio Jornalista Mário Filho"},
        "data": {
            "nickname": "Maracanã",
            "city": "Rio de Janeiro",
            "state": StateEnum.RJ,
            "capacity": 78838,
            "year": 1950,
            "address": "Avenida Maracanã"
        }
    },
    {
        "filter": {"name": "Allianz Parque"},
        "data": {
            "nickname": "Allianz Parque",
            "city": "São Paulo",
            "state": StateEnum.SP,
            "capacity": 43713,
            "year": 2014,
            "address": "Avenida Francisco Matarazzo"
        }
    },
    {
        "filter": {"name": "Arena MRV"},
        "data": {
            "nickname": "Arena MRV",
            "city": "Belo Horizonte",
            "state": StateEnum.MG,
            "capacity": 46000,
            "year": 2023,
            "address": "Rua Cristina Maria de Assis"
        }
    },
    {
        "filter": {"name": "Neo Química Arena"},
        "data": {
            "nickname": "Arena Corinthians",
            "city": "São Paulo",
            "state": StateEnum.SP,
            "capacity": 49000,
            "year": 2014,
            "address": "Avenida Miguel Ignácio Curi"
        }
    },
    {
        "filter": {"name": "Estádio de São Januário"},
        "data": {
            "nickname": "São Januário",
            "city": "Rio de Janeiro",
            "state": StateEnum.RJ,
            "capacity": 21880,
            "year": 1927,
            "address": "Rua General Almério de Moura"
        }
    }
]

TEAMS_DATA = [
    {
        "filter": {"name": "Esporte Clube Vitória"},
        "stadium_name": "Estádio Manoel Barradas",
        "data": {
            "short_name": "Vitória",
            "sigla": "VIT",
            "city": "Salvador",
            "state": StateEnum.BA,
            "colors": ["#000000", "#FF0000"],
            "alcunha": "Leão da Barra",
            "alcunha_color": "Rubro-negro",
            "year": 1899,
            "mascot": "Leão",
            "description": "O Leão da Barra, um dos clubes mais tradicionais do futebol brasileiro."
        }
    },
    {
        "filter": {"name": "Esporte Clube Bahia"},
        "stadium_name": "Arena Fonte Nova",
        "data": {
            "short_name": "Bahia",
            "sigla": "BAH",
            "city": "Salvador",
            "state": StateEnum.BA,
            "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
            "alcunha": "Esquadrão de Aço",
            "alcunha_color": "Tricolor",
            "year": 1931,
            "mascot": "Super-Homem",
            "description": "Bicampeão Brasileiro e primeiro campeão do futebol brasileiro em 1959."
        }
    },
    {
        "filter": {"name": "Clube de Regatas do Flamengo"},
        "stadium_name": "Estádio Jornalista Mário Filho",
        "data": {
            "short_name": "Flamengo",
            "sigla": "FLA",
            "city": "Rio de Janeiro",
            "state": StateEnum.RJ,
            "colors": ["#FF0000", "#000000"],
            "alcunha": "Mengão",
            "alcunha_color": "Rubro-negro",
            "year": 1895,
            "mascot": "Urubu",
            "description": "Clube de maior torcida do Brasil."
        }
    },
    {
        "filter": {"name": "Sociedade Esportiva Palmeiras"},
        "stadium_name": "Allianz Parque",
        "data": {
            "short_name": "Palmeiras",
            "sigla": "PAL",
            "city": "São Paulo",
            "state": StateEnum.SP,
            "colors": ["#008000", "#FFFFFF"],
            "alcunha": "Verdão",
            "alcunha_color": "Alviverde",
            "year": 1914,
            "mascot": "Periquito / Porco",
            "description": "Maior campeão nacional do futebol brasileiro."
        }
    },
    {
        "filter": {"name": "Clube Atlético Mineiro"},
        "stadium_name": "Atlético-MG",
        "stadium_name": "Arena MRV",
        "data": {
            "short_name": "Atlético-MG",
            "sigla": "CAM",
            "city": "Belo Horizonte",
            "state": StateEnum.MG,
            "colors": ["#000000", "#FFFFFF"],
            "alcunha": "Galo",
            "alcunha_color": "Alvinegro",
            "year": 1908,
            "mascot": "Galo",
            "description": "Campeão Brasileiro e da Copa Libertadores da América."
        }
    },
    {
        "filter": {"name": "Sport Club Corinthians Paulista"},
        "stadium_name": "Neo Química Arena",
        "data": {
            "short_name": "Corinthians",
            "sigla": "COR",
            "city": "São Paulo",
            "state": StateEnum.SP,
            "colors": ["#FFFFFF", "#000000"],
            "alcunha": "Timão",
            "alcunha_color": "Alvinegro",
            "year": 1910,
            "mascot": "Mosqueteiro",
            "description": "Bicampeão Mundial de Clubes FIFA."
        }
    },
    {
        "filter": {"name": "Club de Regatas Vasco da Gama"},
        "stadium_name": "Estádio de São Januário",
        "data": {
            "short_name": "Vasco",
            "sigla": "VAS",
            "city": "Rio de Janeiro",
            "state": StateEnum.RJ,
            "colors": ["#000000", "#FFFFFF"],
            "alcunha": "Gigante da Colina",
            "alcunha_color": "Cruzmaltino",
            "year": 1898,
            "mascot": "Almirante",
            "description": "Campeão da Libertadores da América de 1998."
        }
    }
]

async def seed_stadiums_and_teams():
    print(" [1/4] Povoando Estádios e Times...")
    async with AsyncSessionLocal() as session:
        try:
            stadium_map = {}
            for item in STADIUMS_DATA:
                create_data = {**item["data"], "id": uuid.uuid4(), "name": item["filter"]["name"]}
                stadium = await get_or_create(session, Stadium, item["filter"], create_data)
                stadium_map[item["filter"]["name"]] = stadium.id

            for item in TEAMS_DATA:
                st_id = stadium_map.get(item["stadium_name"])
                create_data = {**item["data"], "id": uuid.uuid4(), "name": item["filter"]["name"], "stadium_id": st_id}
                await get_or_create(session, Team, item["filter"], create_data)

            await session.commit()
            print(" Estádios e Times sincronizados com sucesso!")
        except Exception as e:
            print(f"| ERRO | Falha ao povoar estádios e times: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_stadiums_and_teams())