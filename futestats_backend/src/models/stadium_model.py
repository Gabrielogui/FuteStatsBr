from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.models.enums import StateEnum

if TYPE_CHECKING:
    from .team_model import Team

class Stadium(Base):
    __tablename__ = "stadiums"

    name    : Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    city    : Mapped[str] = mapped_column(String(100), nullable=False)
    state   : Mapped[StateEnum] = mapped_column(SAEnum(StateEnum), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    year    : Mapped[int] = mapped_column(Integer)

    teams: Mapped[List["Team"]] = relationship(
        "Team", back_populates="stadium"
    )

    def __repr__(self):
        return f"<Stadium(name={self.name})>"