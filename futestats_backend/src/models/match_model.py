from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from src.db.base import Base
from src.models.enums import MatchStatusEnum

if TYPE_CHECKING:
    from src.models.edition_model import Edition
    from src.models.edition_model import Phase
    from src.models.stadium_model import Stadium
    from src.models.team_model import Team

class Match(Base):
    __tablename__ = "matches"

    date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[MatchStatusEnum] = mapped_column(SAEnum(MatchStatusEnum), default=MatchStatusEnum.SCHEDULED)
    
    # Placar
    home_score: Mapped[int] = mapped_column(Integer, default=0)
    away_score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Chaves Estrangeiras
    edition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("editions.id"))
    phase_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("phases.id"))
    stadium_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("stadiums.id"))
    
    home_team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))

    # Relacionamentos
    edition: Mapped["Edition"] = relationship("Edition", back_populates="matches")
    phase: Mapped["Phase"] = relationship("Phase", back_populates="matches")
    stadium: Mapped[Optional["Stadium"]] = relationship("Stadium")
    home_team: Mapped["Team"] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped["Team"] = relationship("Team", foreign_keys=[away_team_id])