from pydantic import BaseModel
from typing import Optional

class ArtistaCreate(BaseModel):
    nome: str
    genero: str
    data_estreia: str
    sobre: Optional[str] = None

class ArtistaModel(ArtistaCreate):
    id: int
