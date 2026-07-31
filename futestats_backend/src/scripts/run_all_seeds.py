import asyncio
from src.scripts import (
    seed_stadiums_and_teams,
    seed_competitions,
    seed_brasileirao_2024,
    seed_copa_2024,
    seed_hybrid_2024
)

async def run_all():
    print("==================================================")
    print(" INICIANDO POVOAMENTO DO BANCO DE DADOS FUTESTATS ")
    print("==================================================")
    
    await seed_stadiums_and_teams.seed_stadiums_and_teams()
    await seed_competitions.seed_competitions()
    await seed_brasileirao_2024.seed_brasileirao_2024()
    await seed_copa_2024.seed_copa_2024()
    await seed_hybrid_2024.seed_hybrid_2024()

    print("==================================================")
    print(" POVOAMENTO COMPLETO CONCLUÍDO COM SUCESSO! ")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_all())