from pydantic import BaseModel, ConfigDict, computed_field
from uuid import UUID

class PhotoRead(BaseModel):
    id  : UUID
    path: str 

    @computed_field
    @property
    def url(self) -> str:
        # Aqui você garante que o frontend sempre tenha a rota correta
        # sem precisar gravar o domínio no banco de dados.
        return f"/static/images/{self.path}"

    model_config = ConfigDict(from_attributes=True)