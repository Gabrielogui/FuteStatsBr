import asyncio
import uuid
from src.db.session import AsyncSessionLocal
from src.models import Competition
from src.models.enums import CompetitionTypeEnum, RegionEnum
from src.scripts.utils import get_or_create

COMPETITIONS_DATA = [
    {
        "filter": {"name": "Campeonato Brasileiro Série A"},
        "data": {
            "competition_type": CompetitionTypeEnum.LEAGUE,
            "region": RegionEnum.NACIONAL,
            "description": "A principal divisão do futebol profissional do Brasil."
        }
    },
    {
        "filter": {"name": "Copa do Brasil"},
        "data": {
            "competition_type": CompetitionTypeEnum.CUP,
            "region": RegionEnum.NACIONAL,
            "description": "O torneio eliminatório mais democrático do futebol brasileiro."
        }
    }
]

async def seed_competitions():
    print(" [2/4] Povoando Competições Globais...")
    async with AsyncSessionLocal() as session:
        try:
            for item in COMPETITIONS_DATA:
                create_data = {**item["data"], "id": uuid.uuid4(), "name": item["filter"]["name"]}
                await get_or_create(session, Competition, item["filter"], create_data)

            await session.commit()
            print(" Competições sincronizadas com sucesso!")
        except Exception as e:
            print(f"| ERRO | Falha ao povoar competições: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_competitions())