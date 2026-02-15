FROM python:3.13-slim

WORKDIR /app

# Configurações do ambiente Python
# PYTHONDONTWRITEBYTECODE: evita ficheiros .pyc desnecessários
# PYTHONUNBUFFERED: garante que os logs aparecem em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o PYTHONPATH para que o comando uvicorn reconheça o pacote 'src'
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock* ./


RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


COPY src/ src/


EXPOSE 8000


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]