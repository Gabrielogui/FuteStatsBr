from typing import Optional
from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.enums import CompetitionTypeEnum, RegionEnum

class Competition(Base):
    
    __tablename__ = "competitions"

    name            : Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    competition_type: Mapped[CompetitionTypeEnum] = mapped_column(SAEnum(CompetitionTypeEnum), nullable=False) 
    region          : Mapped[RegionEnum] = mapped_column(SAEnum(RegionEnum), nullable=False) 
    description     : Mapped[str] = mapped_column(String(1000))

    def __repr__(self) -> str:
        return f"<Competition(name={self.name})>"
