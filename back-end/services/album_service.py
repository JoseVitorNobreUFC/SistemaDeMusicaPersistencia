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
from utils import logger

ALBUM_CSV_PATH = './data/albuns.csv'
ARTISTA_CSV_PATH = './data/artists.csv'
MUSICA_CSV_PATH = './data/musics.csv'

def get_all_albums():
  if not os.path.exists(ALBUM_CSV_PATH):
    logger.log_error("Arquivo CSV de álbuns não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")
  
  logger.log_info("Buscando todos os albuns")
  return get_all_records(ALBUM_CSV_PATH)

def get_album_by_id(album_id):
  album = get_record_by_id(ALBUM_CSV_PATH, album_id)
  if not album:
    logger.log_error("Erro: Album não encontrado")
    raise HTTPException(status_code=404, detail="Album nao encontrado")
  
  logger.log_info("Buscando album")
  return get_record_by_id(ALBUM_CSV_PATH, album_id)

def check_empty_fields(ordered_data: Dict[str, str]):
  if not ordered_data["nome"]:
    logger.log_error("Erro: Nome nao pode ser vazio")
    raise HTTPException(status_code=400, detail="Nome nao pode ser vazio")
  if not ordered_data["artista_id"]:
    logger.log_error("Erro: Artista nao pode ser vazio")
    raise HTTPException(status_code=400, detail="Artista nao pode ser vazio")
  if not ordered_data["data_lancamento"]:
    logger.log_error("Erro: Data de lancamento nao pode ser vazia")
    raise HTTPException(status_code=400, detail="Data de lancamento nao pode ser vazia")

def create_album(album: AlbumCreate):
  artista = get_record_by_id(ARTISTA_CSV_PATH, int(album.artista_id))
  if not artista:
    logger.log_error("Erro: Não é possivel criar um album referente a um artista que não existe")
    raise HTTPException(status_code=400, detail="Id de Artista não existe") 

  album = AlbumModel(id=get_next_id(ALBUM_CSV_PATH), **album.dict())
  ordered_data: Dict[str, str] = {
        "id": album.id,
        "nome": album.nome,
        "artista_id": album.artista_id,
        "data_lancamento": album.data_lancamento,
        "gravadora": album.gravadora or ""
  }
  check_empty_fields(ordered_data)

  logger.log_info("Album criado com sucesso")
  return create_record(ALBUM_CSV_PATH, ordered_data)

def update_album(album_id: int, album: AlbumCreate):
  album = get_record_by_id(ALBUM_CSV_PATH, album_id)
  if not album:
    logger.log_error("Erro: Album nao encontrado")
    raise HTTPException(status_code=404, detail="Album nao encontrado")
  
  artista = get_record_by_id(ARTISTA_CSV_PATH, int(album.artista_id))
  if not artista:
    logger.log_error("Erro: Não é possivel atualizar um album referente a um artista que não existe")
    raise HTTPException(status_code=400, detail="Id de Artista não existe") 

  ordered_data = {
        "nome": album.nome,
        "artista_id": album.artista_id,
        "data_lancamento": album.data_lancamento,
        "gravadora": album.gravadora or ""
  }
  check_empty_fields(ordered_data)

  logger.log_info("Album atualizado com sucesso")
  return update_record(ALBUM_CSV_PATH, album_id, ordered_data)

def delete_album(album_id: int):
  album = get_record_by_id(ALBUM_CSV_PATH, album_id)
  if not album:
    logger.log_error("Erro: Album nao encontrado")
    raise HTTPException(status_code=404, detail="Album nao encontrado")
  
  artista = get_record_by_id(ARTISTA_CSV_PATH, int(album.artista_id))
  if not artista:
    logger.log_error("Erro: Não é possivel excluir um album referente a um artista que não existe")
    raise HTTPException(status_code=400, detail="Id de Artista não existe") 

  musics = get_all_records(MUSICA_CSV_PATH)
  for musica in musics:
    if int(musica["album_id"]) == album_id:
      logger.log_error("Erro: Não é possivel excluir um album com musicas")
      raise HTTPException(status_code=400, detail="Album possui musicas")

  logger.log_info("Album excluido com sucesso")
  return delete_record(ALBUM_CSV_PATH, album_id)

def export_albums_as_zip() -> str:
  csv_path = './data/albuns.csv'
  if not os.path.exists(csv_path):
    logger.log_error("Arquivo CSV de álbuns não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")

  zip_path = './data/albuns_export.zip'
  convert_file_to_zip(zip_path, [csv_path], arc_names=['albuns.csv'])

  logger.log_info("Zip gerado com sucesso")
  return zip_path

def get_albums_csv_hash():
  csv_path = './data/albuns.csv'
  if not os.path.exists(csv_path):
    logger.log_error("Arquivo CSV de álbuns não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")

  logger.log_info("Hash gerado com sucesso")
  return calculate_file_sha256(csv_path)

def export_albums_as_xml() -> str:
  if not os.path.exists(ALBUM_CSV_PATH):
    logger.log_error("Arquivo CSV de álbuns não encontrado")
    raise HTTPException(status_code=404, detail="Arquivo CSV de álbuns não encontrado")

  xml_path = './data/albuns_export.xml'
  success = convert_csv_to_xml(ALBUM_CSV_PATH, xml_path, root_tag="Albuns", record_tag="Album")
  if not success:
    logger.log_error("Erro ao gerar XML")
    raise HTTPException(status_code=400, detail="Erro ao gerar XML")

  logger.log_info("XML gerado com sucesso")
  return xml_path

def get_album_quantity():
  logger.log_info("Buscando quantidade de álbuns")
  return get_all_albums().__len__()

def search_album(field: str, value: str):
  logger.log_info("Pesquisando álbuns")
  return search_by_field(ALBUM_CSV_PATH, field, value)