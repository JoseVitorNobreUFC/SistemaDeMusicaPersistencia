from utils.generic_crud import (
  get_all_records,
  get_record_by_id,
  create_record,
  update_record,
  delete_record,
  get_next_id,
  convert_file_to_zip,
  calculate_file_sha256,
  convert_csv_to_xml
)
from models.artista_model import ArtistaCreate, ArtistaModel
from typing import Dict
from fastapi import HTTPException
import os

AUTHOR_CSV_PATH = './data/artists.csv'
ALBUM_CSV_PATH = './data/albuns.csv'

def get_all_artists():
  return get_all_records(AUTHOR_CSV_PATH)

def get_artist_by_id(artist_id):
  return get_record_by_id(AUTHOR_CSV_PATH, artist_id)

def create_artist(artist: ArtistaCreate):
  artista = ArtistaModel(id=get_next_id(AUTHOR_CSV_PATH), **artist.dict())
  ordered_data: Dict[str, str] = {
        "id": artista.id,
        "nome": artista.nome,
        "genero": artista.genero,
        "data_estreia": artista.data_estreia,
        "sobre": artista.sobre or ""
  }
  return create_record(AUTHOR_CSV_PATH, ordered_data)

def update_artist(artist_id: int, artist: ArtistaCreate):
  ordered_data = {
        "nome": artist.nome,
        "genero": artist.genero,
        "data_estreia": artist.data_estreia,
        "sobre": artist.sobre or ""
  }
  return update_record(AUTHOR_CSV_PATH, artist_id, ordered_data)

def delete_artist(artist_id: int):
  albuns = get_all_records(ALBUM_CSV_PATH)
  for album in albuns:
    if int(album["artista_id"]) == artist_id:
      raise HTTPException(status_code=400, detail="Artista possui albuns")
  return delete_record(AUTHOR_CSV_PATH, artist_id)

def export_artists_as_zip() -> str:
  csv_path = './data/artists.csv'
  if not os.path.exists(csv_path):
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")

  zip_path = './data/artists_export.zip'
  convert_file_to_zip(zip_path, [csv_path], arc_names=['artists.csv'])
  return zip_path

def get_artists_csv_hash():
  csv_path = './data/artists.csv'
  if not os.path.exists(csv_path):
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")
  return calculate_file_sha256(csv_path)

def export_artists_as_xml() -> str:
  if not os.path.exists(AUTHOR_CSV_PATH):
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")

  xml_path = './data/artists_export.xml'
  success = convert_csv_to_xml(AUTHOR_CSV_PATH, xml_path, root_tag="Artists", record_tag="Artist")
  if not success:
    raise HTTPException(status_code=400, detail="Erro ao gerar XML")

  return xml_path