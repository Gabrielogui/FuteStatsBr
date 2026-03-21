from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PhotoRead(BaseModel):
    id: UUID
    url: str 

    model_config = ConfigDict(from_attributes=True)