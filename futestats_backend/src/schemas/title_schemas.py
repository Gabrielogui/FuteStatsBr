from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from src.schemas.team_schemas import TeamSimpleResponse
from src.schemas.comepetition_schemas import CompetitionRead

# |=======| REQUEST PARA DEFINIR/ATUALIZAR OS CAMPEÕES E VICES DE UMA EDIÇÃO |=======|
class SetEditionChampionsRequest(BaseModel):
    champion_team_ids : List[UUID] = Field(..., min_length=1, description="Lista de IDs dos times campeões")
    runner_up_team_ids: Optional[List[UUID]] = Field(default_factory=list, description="Lista de IDs dos times vices")

# |=======| ITEM DA LINHA DO TEMPO DA GALERIA DE CAMPEÕES DE UMA COMPETIÇÃO |=======|
class EditionChampionItem(BaseModel):
    edition_id  : UUID
    edition_name: str
    year        : int
    champions   : List[TeamSimpleResponse]
    runners_up  : List[TeamSimpleResponse]

    class Config:
        from_attributes = True

# |=======| RESPOSTA COM O HISTÓRICO DE CAMPEÕRES DE UM CAMPEONATO ANO A ANO |=======|
class CompetitionChampionsResponse(BaseModel):
    competition   : CompetitionRead
    total_editions: int
    history       : List[EditionChampionItem]

# |=======| ITEM DE TÍTULO INDIVIDUAL DENTRO DA SALA DE TROFÉU |=======| 
class TitleDetailItem(BaseModel):
    edition_id  : UUID
    edition_name: str
    year        : int
    is_shared   : bool = False # Flag para indicar se o título foi dividido/compartilhado naquele ano

# |=======| RESUMO DOS TÍTULOS DE UM CLUBE AGRUPADOS POR CAMPEONATO |=======|
class TeamTitleSummary(BaseModel):
    competition_id  : UUID
    competition_name: str
    competition_type: str # TODO: COLOCAR ENUM
    region          : str
    total_titles    : int
    editions        : List[TitleDetailItem]

# |=======| RESPOSTA DA SALA DE TROFÉUS DO CLUBE |=======|
class TeamTitlesResponse(BaseModel):
    team                 : TeamSimpleResponse
    total_titles_count   : int
    titles_by_competition: List[TeamTitleSummary]

# |=======| ITEM DO RANKING DOS MAIORES CAMPEÕES DE UMA COMPETIÇÃO |=======|
class TopWinnerItem(BaseModel):
    position    : int
    team        : TeamSimpleResponse
    titles_count: int
    years       : List[int] = Field(..., description="Anos em que o clube foi campeão")

    class Config:
        from_attributes = True

# |=======| RESPOSTA DO RANKING DOS MAIORES CAMPEÕES DE UMA COMPETIÇÃO |=======|
class CompetitionTopWinnersResponse(BaseModel):
    competition   : CompetitionRead
    total_editions: int
    ranking       : List[TopWinnerItem]