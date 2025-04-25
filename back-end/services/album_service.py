from utils.generic_crud import (
  get_all_records,
  get_record_by_id,
  create_record,
  update_record,
  delete_record,
  get_next_id
)
from models.album_model import AlbumCreate, AlbumModel
from typing import Dict
from fastapi import HTTPException

ALBUM_CSV_PATH = './data/albuns.csv'
ARTISTA_CSV_PATH = './data/artists.csv'
MUSICA_CSV_PATH = './data/musics.csv'

def get_all_albums():
  return get_all_records(ALBUM_CSV_PATH)

def get_album_by_id(album_id):
  return get_record_by_id(ALBUM_CSV_PATH, album_id)

def create_album(album: AlbumCreate):
  artista = get_record_by_id(ARTISTA_CSV_PATH, int(album.artista_id))
  if not artista:
    raise HTTPException(status_code=400, detail="Id de Artista não existe") 

  album = AlbumModel(id=get_next_id(ALBUM_CSV_PATH), **album.dict())
  ordered_data: Dict[str, str] = {
        "id": album.id,
        "nome": album.nome,
        "artista_id": album.artista_id,
        "data_lancamento": album.data_lancamento,
        "gravadora": album.gravadora or ""
  }
  return create_record(ALBUM_CSV_PATH, ordered_data)

def update_album(album_id: int, album: AlbumCreate):
  artista = get_record_by_id(ARTISTA_CSV_PATH, int(album.artista_id))
  if not artista:
    raise HTTPException(status_code=400, detail="Id de Artista não existe") 

  ordered_data = {
        "nome": album.nome,
        "artista_id": album.artista_id,
        "data_lancamento": album.data_lancamento,
        "gravadora": album.gravadora or ""
  }
  return update_record(ALBUM_CSV_PATH, album_id, ordered_data)

def delete_album(album_id: int):
  musics = get_all_records(MUSICA_CSV_PATH)
  for musica in musics:
    if int(musica["album_id"]) == album_id:
      raise HTTPException(status_code=400, detail="Album possui musicas")
  return delete_record(ALBUM_CSV_PATH, album_id)

