import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import AsyncSessionLocal
from src.models import Stadium, Team
from src.models.enums import StateEnum

async def seed():
    """
    Script para popular o banco de dados com dados iniciais de teste.
    """
    print("Iniciando seed de dados...")
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Criar um Estádio de teste
            # Usamos uuid4() para gerar IDs únicos
            stadium_id = uuid.uuid4()
            stadium = Stadium(
                id=stadium_id,
                name="Barradão",
                city="Salvador",
                state=StateEnum.BA,
                capacity=35000,
                year=1986
            )
            session.add(stadium)
            
            # 2. Criar um Time associado a esse estádio
            team = Team(
                id=uuid.uuid4(),
                name="Esporte Clube Vitória",
                short_name="Vitória",
                alcunha="Leão da Barra",
                year=1899,
                description="O maior do Nordeste.",
                stadium_id=stadium_id
                # 'colors' removido conforme solicitado
            )
            session.add(team)
            
            # Commit das alterações
            await session.commit()
            print("Dados inseridos com sucesso!")
            
        except Exception as e:
            print(f"| ERRO | Erro ao inserir dados: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    # Inicia o loop de eventos assíncronos para rodar o seed
    asyncio.run(seed())