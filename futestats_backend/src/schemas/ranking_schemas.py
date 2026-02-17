from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import List, Optional

class RankingEntryRead(BaseModel):
    position     : int
    value        : float
    display_value: str
    team_id      : UUID
    
    model_config = ConfigDict(from_attributes=True)

class RankingCategoryBase(BaseModel):
    slug        : str = Field(..., description="O slug da categoria", examples=["mias-gols-brasileirao"])
    name        : str = Field(..., description="O nome da categoria", examples=["Mias Gols Brasileirao"])
    description : Optional[str] = None

class RankingCategoryRead(RankingCategoryBase):
    id: UUID
    entries: List[RankingEntryRead] = []

    model_config = ConfigDict(from_attributes=True)