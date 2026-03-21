from uuid import UUID
from typing import List, Sequence
from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.image_model import Photo

class ImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def get_images(self, entity_type: str, entity_id: UUID) -> Sequence[Photo]:
        query = select(Photo).where(
            Photo.entity_type == entity_type.upper(), 
            Photo.entity_id == entity_id
        )

        result = await self.session.execute(query)
        return result.scalars().all()
    

    # Insere múltiplos registros de fotos e retorna seus IDs
    async def insert_images(self, entity_type: str, entity_id: UUID, image_paths: List[str]) -> List[UUID]:
        if not image_paths:
            return []
            
        values = [
            {"entity_type": entity_type.upper(), "entity_id": entity_id, "path": path} 
            for path in image_paths
        ]
        
        query = insert(Photo).values(values).returning(Photo.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    # Remove uma imagem pelo seu ID
    async def delete_image(self, img_id: UUID) -> bool:
        query = delete(Photo).where(Photo.id == img_id)
        result = await self.session.execute(query)
        return result.rowcount > 0

    # Remove todas as referências de imagens de uma entidade no banco de dados
    async def delete_entity_images(self, entity_type: str, entity_id: UUID) -> None:
        query = delete(Photo).where(
            Photo.entity_type == entity_type.upper(), 
            Photo.entity_id == entity_id
        )
        await self.session.execute(query)