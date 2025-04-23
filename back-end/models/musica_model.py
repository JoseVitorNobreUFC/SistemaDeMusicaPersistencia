from pydantic import BaseModel

class Musica(BaseModel):
  id: int
  nome: str
  album_id: int
  data_lancamento: str ## Passar pra DateTime depois
  duracao: int