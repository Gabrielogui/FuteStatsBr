from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from src.db.base import Base

from src.models.enums import StateEnum

if TYPE_CHECKING:
    from .stadium_model import Stadium

class Team(Base):
    __tablename__ = "teams"

    name       : Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    short_name : Mapped[str] = mapped_column(String(100), index=True)
    sigla      : Mapped[str] = mapped_column(String(100))
    city       : Mapped[str] = mapped_column(String(100))
    state      : Mapped[StateEnum] = mapped_column(SAEnum(StateEnum), nullable=False)

    colors       : Mapped[List[str]] = mapped_column(String(100))
    alcunha      : Mapped[str] = mapped_column(String(100))
    alcunha_color: Mapped[str] = mapped_column(String(100))
    year         : Mapped[int] = mapped_column(Integer)
    mascot       : Mapped[str] = mapped_column(String(100))
    description  : Mapped[str] = mapped_column(String(1000))

    subscribers_count: Mapped[int] = mapped_column(Integer, default=0)

    stadium_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("stadiums.id"))
    stadium: Mapped[Optional["Stadium"]] = relationship("Stadium", back_populates="teams")

    def __repr__(self):
        return f"<Team(name={self.name})>"
