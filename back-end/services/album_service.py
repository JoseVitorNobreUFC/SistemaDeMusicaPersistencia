from utils.generic_crud import (
  get_all_records,
  get_record_by_id,
  create_record,
  update_record,
  delete_record,
  get_next_id,
  convert_file_to_zip,
  calculate_file_sha256,
  convert_csv_to_xml,
  search_by_field
)
from models.album_model import AlbumCreate, AlbumModel
from typing import Dict
from fastapi import HTTPException
import os

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

def export_albums_as_zip() -> str:
  csv_path = './data/albuns.csv'
  if not os.path.exists(csv_path):
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")

  zip_path = './data/albuns_export.zip'
  convert_file_to_zip(zip_path, [csv_path], arc_names=['albuns.csv'])
  return zip_path

def get_albums_csv_hash():
  csv_path = './data/albuns.csv'
  if not os.path.exists(csv_path):
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")
  return calculate_file_sha256(csv_path)

def export_albums_as_xml() -> str:
  if not os.path.exists(ALBUM_CSV_PATH):
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")

  xml_path = './data/albuns_export.xml'
  success = convert_csv_to_xml(ALBUM_CSV_PATH, xml_path, root_tag="Albuns", record_tag="Album")
  if not success:
    raise HTTPException(status_code=400, detail="Erro ao gerar XML")

  return xml_path

def get_album_quantity():
  return get_all_albums().__len__()

def search_album(field: str, value: str):
  return search_by_field(ALBUM_CSV_PATH, field, value)