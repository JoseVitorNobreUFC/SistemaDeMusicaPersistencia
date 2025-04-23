from pydantic import BaseModel

class Album(BaseModel):
  id: int
  nome: str
  artista_id: int
  data_lancamento: str ## Passar pra DateTime depois
  gravadora: str