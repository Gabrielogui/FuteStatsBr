from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from src.models.enums import StateEnum

class StadiumBase(BaseModel):
    name     : str = Field(..., description="O nome do estádio", examples=["Barradão"])
    nickname : str = Field(..., description="O apelido do estádio", examples=["Barradão"])
    city     : str = Field(..., description="A cidade do estádio", examples=["Salvador"])
    state    : StateEnum = Field(..., description="O sigla do estado do estádio")
    capacity : int = Field(..., description="A capacidade do estádio", examples=[35000])
    year     : Optional[int] = Field(..., description="O ano de fundação do estádio", examples=[1900])
    address  : Optional[str] = Field(..., description="O endereço do estádio", examples=["Avenida Paulista, 1000"])

class StadiumCreate(StadiumBase):
    pass

class StadiumUpdate(StadiumBase):
    name    : Optional[str] = None
    city    : Optional[str] = None
    state   : Optional[StateEnum] = None
    capacity: Optional[int] = None

class StadiumRead(StadiumBase):
    id        : UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)