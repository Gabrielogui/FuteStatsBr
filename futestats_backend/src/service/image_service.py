import os
import shutil
import uuid
from uuid import UUID
from typing import List, Dict, Any

from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.image_repository import ImageRepository
from src.models.enums import EntityTypesEnum

class ImageService:

    IMAGE_BASE_PATH = "src/static/images"

    def __init__(self, session: AsyncSession):
        self.repository = ImageRepository(session)


    # GERENCIA O UPLOAD DE IMAGENS DE UMA ENTIDADE NO TIPO FÍSICO
    async def upload_entity_images(self, entity_type: EntityTypesEnum, entity_id: UUID, files: List[UploadFile], request: Request) -> List[UUID]:
        
        # Organização de pastas: src/static/images/{entity_type}/{entity_id}
        entity_folder = entity_type.value.lower()
        folder_path = os.path.join(self.IMAGE_BASE_PATH, entity_folder, str(entity_id))
        os.makedirs(folder_path, exist_ok=True)

        image_paths = []
        base_url = str(request.url).rstrip("/")

        for file in files:
            ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
            unique_name = f"{uuid.uuid4().hex}{ext}"

            file_disk_path = os.path.join(folder_path, unique_name)
            db_relative_path = f"{entity_folder}/{entity_id}/{unique_name}"

            # Leitura e escrita eficiente do arquivo:
            content = await file.read()
            with open(file_disk_path, "wb") as buffer:
                buffer.write(content)

            image_paths.append(db_relative_path)

        image_ids = await self.repository.insert_images(entity_type, entity_id, image_paths)
        
        return [
            {"id": img_id, "url": f"{base_url}/static/images/{path}"}
            for img_id, path in zip(image_ids, image_paths)
        ]

    
    async def get_images_by_entity(self, entity_type: str, entity_id: UUID, request: Request) -> List[Dict[str, Any]]:
        images = await self.repository.get_images(entity_type, entity_id)
        base_url = str(request.base_url).rstrip("/")
        
        return [
            {"id": img.id, "url": f"{base_url}/static/images/{img.path}"} 
            for img in images
        ]
    
    # LIMPEZA COMPLETA: REMOVE REGISTROS DO BANCO E DELETA A PASTA NO DISCO
    async def delete_all_entity_photos(self, entity_type: str, entity_id: UUID) -> None:
        # 1. Banco de dados
        await self.repository.delete_entity_images(entity_type, entity_id)
        
        # 2. Disco rígido
        folder_path = os.path.join(self.IMAGE_BASE_PATH, entity_type.lower(), str(entity_id))
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)
