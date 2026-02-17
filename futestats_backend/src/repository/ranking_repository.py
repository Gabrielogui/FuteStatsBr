from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.base_repository import BaseRepository
from src.models.ranking_model import RankingCategory, RankingEntry

import uuid

class RankingRepository(BaseRepository[RankingCategory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RankingCategory, session)

    async def get_by_slug(self, slug: str) -> Optional[RankingCategory]:
        """
        Busca uma categoria de ranking pelo slug e já traz as entradas 
        e os respectivos times (Join triplo assíncrono).
        """
        query = (
            select(RankingCategory)
            .where(RankingCategory.slug == slug)
            .options(
                selectinload(RankingCategory.entries)
                .joinedload(RankingEntry.team)
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_categories(self) -> Sequence[RankingCategory]:
        query = select(RankingCategory)
        result = await self.session.execute(query)
        return result.scalars().all()

class RankingEntryRepository(BaseRepository[RankingEntry]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RankingEntry, session)

    async def get_entries_by_category(self, category_id: uuid.UUID) -> Sequence[RankingEntry]:
        query = (
            select(RankingEntry)
            .where(RankingEntry.category_id == category_id)
            .options(joinedload(RankingEntry.team))
            .order_by(RankingEntry.position)
        )
        result = await self.session.execute(query)
        return result.scalars().all()