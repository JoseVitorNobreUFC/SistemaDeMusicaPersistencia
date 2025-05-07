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
from models.artista_model import ArtistaCreate, ArtistaModel
from typing import Dict
from fastapi import HTTPException
import os
from utils import logger

AUTHOR_CSV_PATH = './data/artists.csv'
ALBUM_CSV_PATH = './data/albuns.csv'

def get_all_artists():
  if not os.path.exists(AUTHOR_CSV_PATH):
    logger.log_error("Arquivo CSV de artistas nao encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas nao encontrado")

  logger.log_info("Buscando todos os artistas")
  return get_all_records(AUTHOR_CSV_PATH)

def get_artist_by_id(artist_id):
  artist = get_record_by_id(AUTHOR_CSV_PATH, artist_id)
  if not artist:
    logger.log_error("Erro: Artista nao encontrado")
    raise HTTPException(status_code=400, detail="Id de Artista nao encontrado")

  logger.log_info("Buscando artista")
  return artist

def check_empty_fields(ordered_data: Dict[str, str]):
  if not ordered_data["nome"]:
    logger.log_error("Erro: Nome nao pode ser vazio")
    raise HTTPException(status_code=400, detail="Nome nao pode ser vazio")
  if not ordered_data["genero"]:
    logger.log_error("Erro: Genero nao pode ser vazio")
    raise HTTPException(status_code=400, detail="Genero nao pode ser vazio")
  if not ordered_data["data_estreia"]:
    logger.log_error("Erro: Data de estreia nao pode ser vazia")
    raise HTTPException(status_code=400, detail="Data de estreia nao pode ser vazia")


def create_artist(artist: ArtistaCreate):
  artista = ArtistaModel(id=get_next_id(AUTHOR_CSV_PATH), **artist.dict())
  ordered_data: Dict[str, str] = {
        "id": artista.id,
        "nome": artista.nome,
        "genero": artista.genero,
        "data_estreia": artista.data_estreia,
        "sobre": artista.sobre or ""
  }
  
  check_empty_fields(ordered_data)

  logger.log_info("Artista criado com sucesso")
  return create_record(AUTHOR_CSV_PATH, ordered_data)

def update_artist(artist_id: int, artist: ArtistaCreate):
  artista = get_record_by_id(AUTHOR_CSV_PATH, artist_id)
  if not artista:
    logger.log_error("Erro: Artista nao encontrado")
    raise HTTPException(status_code=404, detail="Artista nao encontrado")

  ordered_data = {
        "nome": artist.nome,
        "genero": artist.genero,
        "data_estreia": artist.data_estreia,
        "sobre": artist.sobre or ""
  }

  check_empty_fields(ordered_data)

  logger.log_info("Artista atualizado com sucesso")
  return update_record(AUTHOR_CSV_PATH, artist_id, ordered_data)

def delete_artist(artist_id: int):
  artista = get_record_by_id(AUTHOR_CSV_PATH, artist_id)
  if not artista:
    logger.log_error("Erro: Artista nao encontrado")
    raise HTTPException(status_code=404, detail="Artista nao encontrado")

  albuns = get_all_records(ALBUM_CSV_PATH)
  for album in albuns:
    if int(album["artista_id"]) == artist_id:
      logger.log_error("Erro: Não é possivel excluir um artista com albuns")
      raise HTTPException(status_code=400, detail="Artista possui albuns")
    
  logger.log_info("Artista excluido com sucesso")
  return delete_record(AUTHOR_CSV_PATH, artist_id)

def export_artists_as_zip() -> str:
  csv_path = './data/artists.csv'
  if not os.path.exists(csv_path):
    logger.log_error("Arquivo CSV de artistas não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")

  zip_path = './data/artists_export.zip'
  convert_file_to_zip(zip_path, [csv_path], arc_names=['artists.csv'])

  logger.log_info("Zip gerado com sucesso")
  return zip_path

def get_artists_csv_hash():
  csv_path = './data/artists.csv'
  if not os.path.exists(csv_path):
    logger.log_error("Arquivo CSV de artistas não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")

  logger.log_info("Hash gerado com sucesso")
  return calculate_file_sha256(csv_path)

def export_artists_as_xml() -> str:
  if not os.path.exists(AUTHOR_CSV_PATH):
    raise HTTPException(status_code=404, detail="Arquivo CSV de artistas não encontrado")

  xml_path = './data/artists_export.xml'
  success = convert_csv_to_xml(AUTHOR_CSV_PATH, xml_path, root_tag="Artists", record_tag="Artist")
  if not success:
    logger.log_error("Erro ao gerar XML")
    raise HTTPException(status_code=400, detail="Erro ao gerar XML")

  logger.log_info("XML gerado com sucesso")
  return xml_path

def get_artists_quantity():
  logger.log_info("Buscando quantidade de artistas")
  return get_all_artists().__len__()

def search_artist(field: str, value: str):
  logger.log_info("Pesquisando artistas")
  return search_by_field(AUTHOR_CSV_PATH, field, value)