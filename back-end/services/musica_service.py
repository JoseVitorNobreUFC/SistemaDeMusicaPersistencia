from utils.generic_crud import (
    get_all_records,
    get_record_by_id,
    create_record,
    update_record,
    delete_record,
    get_next_id
)
from models.musica_model import MusicaCreate, MusicaModel
from typing import Dict

MUSIC_CSV_PATH = './data/musics.csv'

def get_all_musics():
    return get_all_records(MUSIC_CSV_PATH)

def get_music_by_id(music_id: int):
    return get_record_by_id(MUSIC_CSV_PATH, music_id)

def create_music(music: MusicaCreate):
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
    ordered_data = {
        "nome": music.nome,
        "id_album": music.id_album,
        "data_lancamento": music.data_lancamento,
        "duracao": music.duracao or ""
    }
    return update_record(MUSIC_CSV_PATH, music_id, ordered_data)

def delete_music(music_id: int):
    return delete_record(MUSIC_CSV_PATH, music_id)
