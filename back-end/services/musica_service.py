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
from models.musica_model import MusicaCreate, MusicaModel
from typing import Dict
from fastapi import HTTPException
import os

MUSIC_CSV_PATH = './data/musics.csv'
ALBUM_CSV_PATH = './data/albuns.csv'

def get_all_musics():
    return get_all_records(MUSIC_CSV_PATH)

def get_music_by_id(music_id: int):
    return get_record_by_id(MUSIC_CSV_PATH, music_id)

def create_music(music: MusicaCreate):
    album = get_record_by_id(ALBUM_CSV_PATH, int(music.id_album))
    if not album:
        raise HTTPException(status_code=400, detail="Id de Album não existe")
    musica = MusicaModel(id=get_next_id(MUSIC_CSV_PATH), **music.dict())
    ordered_data: Dict[str, str] = {
        "id": musica.id,
        "nome": musica.nome,
        "id_album": musica.id_album,
        "data_lancamento": musica.data_lancamento,
        "duracao": musica.duracao or ""
    }
    return create_record(MUSIC_CSV_PATH, ordered_data)

def update_music(music_id: int, music: MusicaCreate):
    album = get_record_by_id(ALBUM_CSV_PATH, int(music.id_album))
    if not album:
        raise HTTPException(status_code=400, detail="Id de Album não existe")
    ordered_data = {
        "nome": music.nome,
        "id_album": music.id_album,
        "data_lancamento": music.data_lancamento,
        "duracao": music.duracao or ""
    }
    return update_record(MUSIC_CSV_PATH, music_id, ordered_data)

def delete_music(music_id: int):
    return delete_record(MUSIC_CSV_PATH, music_id)

def export_musics_as_zip() -> str:
    csv_path = './data/musics.csv'
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")

    zip_path = './data/musics_export.zip'
    convert_file_to_zip(zip_path, [csv_path], arc_names=['musics.csv'])
    return zip_path

def get_musics_csv_hash():
    csv_path = './data/musics.csv'
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")
    return calculate_file_sha256(csv_path)

def export_musics_as_xml() -> str:
    if not os.path.exists(MUSIC_CSV_PATH):
        raise HTTPException(status_code=404, detail="Arquivo CSV de músicas não encontrado")
    
    xml_path = './data/musics_export.xml'
    success = convert_csv_to_xml(MUSIC_CSV_PATH, xml_path, root_tag="Musicas", record_tag="Musica")
    if not success:
        raise HTTPException(status_code=400, detail="Erro ao gerar XML")

    return xml_path