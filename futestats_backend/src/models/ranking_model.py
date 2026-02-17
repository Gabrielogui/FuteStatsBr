from typing import List, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
import uuid

if TYPE_CHECKING:
    from src.models.team_model import Team

class RankingCategory(Base):
    __tablename__ = "ranking_categories"

    slug       : Mapped[str] = mapped_column(String(50), unique=True, index=True) 
    name       : Mapped[str] = mapped_column(String(100)) 
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relacionamento: Uma categoria tem várias entradas (os times no ranking)
    entries: Mapped[List["RankingEntry"]] = relationship(
        "RankingEntry", 
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin" # Carrega as entradas de forma eficiente em consultas assíncronas
    )

    def __repr__(self):
        return f"RankingCategory(slug={self.slug}, name={self.name})"



class RankingEntry(Base):
    """
    Entradas específicas de um ranking. 
    Relaciona um time a uma posição e valor em uma categoria específica.
    """
    __tablename__ = "ranking_entries"

    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ranking_categories.id"), nullable=False)
    team_id    : Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
    
    position     : Mapped[int] = mapped_column(Integer, nullable=False)
    value        : Mapped[float] = mapped_column(Float, nullable=False) 
    display_value: Mapped[str] = mapped_column(String(50), nullable=False) 

    # |=======| RELACIONAMENTOS |=======|
    # Relacionamento com categoria
    category: Mapped["RankingCategory"] = relationship("RankingCategory", back_populates="entries")
    
    # Relacionamento com o Time para podermos acessar nome e escudo facilmente
    team: Mapped["Team"] = relationship("Team", lazy="joined")

    def __repr__(self) -> str:
        return f"<RankingEntry(pos={self.position}, value={self.display_value})>"