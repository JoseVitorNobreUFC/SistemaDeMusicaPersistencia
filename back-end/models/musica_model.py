from pydantic import BaseModel
from typing import Optional

class MusicaCreate(BaseModel):
    nome: str
    id_album: str
    data_lancamento: str
    duracao: Optional[str] = None

class MusicaModel(MusicaCreate):
    id: number