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
from models.musica_model import MusicaCreate, MusicaModel
from typing import Dict
from fastapi import HTTPException
import os
from utils import logger

MUSIC_CSV_PATH = './data/musics.csv'
ALBUM_CSV_PATH = './data/albuns.csv'

def get_all_musics():
    if not os.path.exists(MUSIC_CSV_PATH):
        logger.log_error("Arquivo CSV de músicas nao encontrado")
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas nao encontrado")
    
    logger.log_info("Buscando todas as músicas")
    return get_all_records(MUSIC_CSV_PATH)

def get_music_by_id(music_id: int):
    music = get_record_by_id(MUSIC_CSV_PATH, music_id)
    if not music:
        logger.log_error("Erro: Musica nao encontrada")
        raise HTTPException(status_code=404, detail="Música nao encontrada")

    logger.log_info("Buscando musica")
    return music

def check_empty_fields(ordered_data: Dict[str, str]):
    empty_fields = []
    if not ordered_data["nome"]:
        empty_fields.append("nome")
    if not ordered_data["id_album"]:
        empty_fields.append("id_album")
    if not ordered_data["data_lancamento"]:
        empty_fields.append("data_lancamento")

    if empty_fields:
        logger.log_error(f"Erro: Campos {', '.join(empty_fields)} nao podem ser vazios")
        raise HTTPException(status_code=400, detail=f"Campos {', '.join(empty_fields)} nao podem ser vazios")

def create_music(music: MusicaCreate):
    album = get_record_by_id(ALBUM_CSV_PATH, int(music.id_album))
    if not album:
        logger.log_error("Erro: Album nao encontrado")
        raise HTTPException(status_code=400, detail="Id de Album não existe")

    musica = MusicaModel(id=get_next_id(MUSIC_CSV_PATH), **music.dict())
    ordered_data: Dict[str, str] = {
        "id": musica.id,
        "nome": musica.nome,
        "id_album": musica.id_album,
        "data_lancamento": musica.data_lancamento,
        "duracao": musica.duracao or ""
    }
    check_empty_fields(ordered_data)

    logger.log_info("Musica criada com sucesso")
    return create_record(MUSIC_CSV_PATH, ordered_data)

def update_music(music_id: int, music: MusicaCreate):
    music = get_record_by_id(MUSIC_CSV_PATH, music_id)
    if not music:
        logger.log_error("Erro: Musica nao encontrada")
        raise HTTPException(status_code=404, detail="Música nao encontrada")

    album = get_record_by_id(ALBUM_CSV_PATH, int(music.id_album))
    if not album:
        logger.log_error("Erro: Album nao encontrado")
        raise HTTPException(status_code=400, detail="Id de Album não existe")

    ordered_data = {
        "nome": music.nome,
        "id_album": music.id_album,
        "data_lancamento": music.data_lancamento,
        "duracao": music.duracao or ""
    }
    check_empty_fields(ordered_data)

    logger.log_info("Musica atualizada com sucesso")
    return update_record(MUSIC_CSV_PATH, music_id, ordered_data)

def delete_music(music_id: int):
    music = get_record_by_id(MUSIC_CSV_PATH, music_id)
    if not music:
        logger.log_error("Erro: Musica nao encontrada")
        raise HTTPException(status_code=404, detail="Música nao encontrada")

    album = get_record_by_id(ALBUM_CSV_PATH, int(music.id_album))
    if not album:
        logger.log_error("Erro: Album nao encontrado")
        raise HTTPException(status_code=400, detail="Id de Album não existe")

    logger.log_info("Musica excluida com sucesso")
    return delete_record(MUSIC_CSV_PATH, music_id)

def export_musics_as_zip() -> str:
    csv_path = './data/musics.csv'
    if not os.path.exists(csv_path):
        logger.log_error("Arquivo CSV de músicas não encontrado")
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")

    zip_path = './data/musics_export.zip'
    convert_file_to_zip(zip_path, [csv_path], arc_names=['musics.csv'])

    logger.log_info("Zip gerado com sucesso")
    return zip_path

def get_musics_csv_hash():
    csv_path = './data/musics.csv'
    if not os.path.exists(csv_path):
        logger.log_error("Arquivo CSV de músicas não encontrado")
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")

    logger.log_info("Hash gerado com sucesso")
    return calculate_file_sha256(csv_path)

def export_musics_as_xml() -> str:
    if not os.path.exists(MUSIC_CSV_PATH):
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")
    
    xml_path = './data/musics_export.xml'
    success = convert_csv_to_xml(MUSIC_CSV_PATH, xml_path, root_tag="Musicas", record_tag="Musica")
    if not success:
        logger.log_error("Erro ao gerar XML")
        raise HTTPException(status_code=400, detail="Erro ao gerar XML")

    logger.log_info("XML gerado com sucesso")
    return xml_path

def get_musics_quantity():
    logger.log_info("Quantidade de músicas")
    return get_all_musics().__len__()

def search_music(field: str, value: str):
  logger.log_info("Pesquisando músicas")
  return search_by_field(MUSIC_CSV_PATH, field, value)