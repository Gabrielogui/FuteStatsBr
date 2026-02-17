import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# --- CONFIGURAÇÃO DE PATH PARA ENCONTRAR O PACOTE 'src' ---
import os
import sys

# Adiciona o diretório pai ao sys.path para que o Alembic encontre o módulo 'src'
# Isso permite que os imports abaixo (from src...) funcionem
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Agora importamos os componentes do seu projeto
from src.db.base import Base
from src.core.config import settings
# IMPORTANTE: Importar todos os modelos para que o autogenerate detecte as tabelas
from src.models.stadium_model import Stadium
from src.models.team_model import Team
from src.models.competition_model import Competition
from src.models.ranking_model import RankingCategory, RankingEntry

# Objeto de configuração do Alembic
config = context.config

# Injeta a URL do banco de dados das configurações do seu projeto (.env)
# Isso ignora o que estiver escrito no alembic.ini e usa o seu .env real
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configura o log se o arquivo de config existir
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata para o autogenerate (compara o banco com o código)
target_metadata = Base.metadata

def do_run_migrations(connection: Connection) -> None:
    """Executa as migrações no contexto de uma conexão síncrona."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Cria o engine assíncrono e executa as migrações."""
    configuration = config.get_section(config.config_ini_section, {})
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # run_sync executa a função de migração síncrona dentro do loop assíncrono
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Roda as migrações no modo 'online' (conectado ao banco)."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()