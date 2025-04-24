from fastapi import APIRouter, HTTPException
from models.musica_model import MusicaCreate
from services import musica_service

router = APIRouter()

@router.get("/")
def get_all_musics():
    return musica_service.get_all_musics()

@router.get("/{music_id}")
def get_music_by_id(music_id: int):
    music = musica_service.get_music_by_id(music_id)
    if not music:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return music

@router.post("/")
def create_music(music: MusicaCreate):
    return musica_service.create_music(music)

@router.put("/{music_id}")
def update_music(music_id: int, music: MusicaCreate):
    success = musica_service.update_music(music_id, music)
    if not success:
        raise HTTPException(status_code=404, detail="Música não encontrada para atualização")
    return {"message": "Música atualizada com sucesso"}

@router.delete("/{music_id}")
def delete_music(music_id: int):
    success = musica_service.delete_music(music_id)
    if not success:
        raise HTTPException(status_code=404, detail="Música não encontrada para exclusão")
    return {"message": "Música excluída com sucesso"}
