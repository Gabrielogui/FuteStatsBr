from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, TypeVar, Optional, Dict, Any

T = TypeVar("T")

async def get_or_create(
    session: AsyncSession, 
    model: Type[T], 
    filter_kwargs: Dict[str, Any], 
    create_kwargs: Dict[str, Any]
) -> T:
    """
    Busca um registro no banco pelos parâmetros informados em filter_kwargs.
    Se não encontrar, cria um novo registro com create_kwargs.
    """
    query = select(model).filter_by(**filter_kwargs)
    result = await session.execute(query)
    instance = result.scalar_one_or_none()

    if instance:
        return instance
    else:
        new_instance = model(**create_kwargs)
        session.add(new_instance)
        await session.flush()
        return new_instance