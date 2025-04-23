from fastapi import FastAPI
from controllers import artista_controller, album_controller
import os
import csv
app = FastAPI()


@app.get("/")
async def root():
  return {"message": "Hello World"}

app.include_router(artista_controller.router, prefix="/artistas", tags=["Artistas"])
app.include_router(album_controller.router, prefix="/albuns", tags=["Albuns"])


# Função que verifica se o arquivo CSV existe e cria um se ele não existir
def ensure_csv_exists(filename: str, fieldnames: list):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# Função que é executada quando o servidor inicia
@app.on_event("startup")
def startup_event():
    ensure_csv_exists("data/artists.csv", ["id", "nome", "genero", "data_estreia", "sobre"])
    ensure_csv_exists("data/albuns.csv", ["id", "nome", "artista_id", "data_lancamento", "gravadora"])
    ensure_csv_exists("data/musics.csv", ["id", "nome", "album_id", "data_lancamento", "duracao"])