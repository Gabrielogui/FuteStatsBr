from sqlalchemy import String, ENUM as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.models.enums import EntityTypesEnum

from src.db.base import Base

class Photo(Base):

    __tablename__ = "photos"

    path       : Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[EntityTypesEnum] = mapped_column(SAEnum(EntityTypesEnum), nullable=False)
    entity_id  : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    def __repr__(self):
        return f"<Photo(path={self.path}, entity_type={self.entity_type}, entity_id={self.entity_id})>"