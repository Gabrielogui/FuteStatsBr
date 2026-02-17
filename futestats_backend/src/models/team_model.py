from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from src.db.base import Base

if TYPE_CHECKING:
    from .stadium_model import Stadium

class Team(Base):
    __tablename__ = "teams"

    name       : Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    short_name : Mapped[str] = mapped_column(String(100), index=True)
    alcunha    : Mapped[str] = mapped_column(String(100))
    year       : Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(1000))

    stadium_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("stadiums.id"))
    stadium: Mapped[Optional["Stadium"]] = relationship("Stadium", back_populates="teams")

    def __repr__(self):
        return f"<Team(name={self.name})>"
