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
                name="Estádio Manoel Barradas",
                nickname="Barradão",
                city="Salvador",
                state=StateEnum.BA,
                capacity=35000,
                year=1986,
                address="Avenida Artêmio valente, 0000"
            )
            session.add(stadium)
            
            # 2. Criar um Time associado a esse estádio
            team = Team(
                id=uuid.uuid4(),
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
                description="O maior clube de futebol do Nordeste. Revelou diversos jogadores, como David Luiz e Hulk. Nasceu em 1899 em Salvador - BA.",
                stadium_id=stadium_id
                
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