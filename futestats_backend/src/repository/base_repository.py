from typing import Generic, Type, TypeVar, List, Optional, Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.db.base import Base
import uuid

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: uuid.UUID) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: Any) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(exclude_unset=True))
        self.session.add(db_obj)
        await self.session.flush() 
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: Any) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, id: uuid.UUID) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        # rowcount indica quantas linhas foram afetadas
        return result.rowcount > 0