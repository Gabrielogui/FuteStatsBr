from typing import Optional,  List, TYPE_CHECKING
from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.models.enums import CompetitionTypeEnum, RegionEnum

if TYPE_CHECKING:
    from src.models.edition_model import Edition


class Competition(Base):
    
    __tablename__ = "competitions"

    name            : Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    competition_type: Mapped[CompetitionTypeEnum] = mapped_column(SAEnum(CompetitionTypeEnum), nullable=False) 
    region          : Mapped[RegionEnum] = mapped_column(SAEnum(RegionEnum), nullable=False) 
    description     : Mapped[str] = mapped_column(String(1000))

    editions: Mapped[List["Edition"]] = relationship(
        "Edition", 
        back_populates="competition", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Competition(name={self.name})>"

# TODO: ADICIONAR RELAÇÃO COM UMA FUTURA TABELA DE TROFÉUS - Uma competição ter uma lista de troféus
