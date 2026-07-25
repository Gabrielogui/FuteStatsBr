from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import JSON, String, Integer, ForeignKey, Table, Column, Date, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from src.db.base import Base
from src.models.enums import EditionFormatEnum

if TYPE_CHECKING:
    from src.models.competition_model import Competition
    from src.models.edition_model import Phase
    from src.models.match_model import Match
    from src.models.team_model import Team

# Tabela associativa para Times em uma Edição
edition_teams = Table(
    "edition_teams",
    Base.metadata,
    Column("edition_id", ForeignKey("editions.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)

class Edition(Base):
    __tablename__ = "editions"

    name  : Mapped[str] = mapped_column(String(100)) # Ex: "Campeonato Brasileiro 2003"
    year  : Mapped[int] = mapped_column(Integer)
    format: Mapped[EditionFormatEnum] = mapped_column(SAEnum(EditionFormatEnum))
    
    competition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competitions.id"))

    # Configuração do refulamento da edição
    relegated_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    rules_config   : Mapped[Optional[dict]] = mapped_column(JSON, nullable=True) # Ex: {"g4_direct": 4, "pre_libertadores": 2}
    
    # Relacionamentos
    competition: Mapped["Competition"] = relationship("Competition", back_populates="editions")
    teams      : Mapped[List["Team"]] = relationship("Team", secondary=edition_teams)
    phases     : Mapped[List["Phase"]] = relationship("Phase", back_populates="edition", cascade="all, delete-orphan")
    matches    : Mapped[List["Match"]] = relationship("Match", back_populates="edition")

class Phase(Base):
    __tablename__ = "phases"

    name      : Mapped[str] = mapped_column(String(100)) # Ex: "Primeiro Turno", "Quartas de Final"
    order     : Mapped[int] = mapped_column(Integer)    # Para ordenar cronologicamente
    edition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("editions.id"))
    
    edition: Mapped["Edition"] = relationship("Edition", back_populates="phases")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="phase")

    rounds: Mapped[List["Round"]] = relationship("Round", back_populates="phase", cascade="all, delete-orphan")


class Round(Base):
    __tablename__ = "rounds"

    number  : Mapped[int] = mapped_column(Integer, nullable=False) # Ex: 1, 2, 3... 38
    name    : Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # Ex: "1ª Rodada"
    phase_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("phases.id", ondelete="CASCADE"))

    # Relacionamentos
    phase  : Mapped["Phase"] = relationship("Phase", back_populates="rounds")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="round", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Round(number={self.number}, phase_id={self.phase_id})>"