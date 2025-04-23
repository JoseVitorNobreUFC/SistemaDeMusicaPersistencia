from pydantic import BaseModel
from typing import Optional

class AlbumCreate(BaseModel):
    nome: str
    artista_id: str
    data_lancamento: str
    gravadora: Optional[str] = None

class AlbumModel(AlbumCreate):
    id: int