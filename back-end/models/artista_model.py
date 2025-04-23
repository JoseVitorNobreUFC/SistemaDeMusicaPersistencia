from pydantic import BaseModel

class Artista(BaseModel):
  id: int
  nome: str
  genero: str
  data_estreia: str ## Passar pra DateTime depois
  sobre: str