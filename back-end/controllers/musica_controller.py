from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from models.musica_model import MusicaCreate
from services import musica_service
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/")
def get_all_musics():
    return musica_service.get_all_musics()

@router.get("/visualizar/quantidade")
def get_musics_count():
    return {"quantidade": musica_service.get_musics_quantity()}

@router.get("/search")
def search_music(field: str = Query(...), value: str = Query(...)):
    return musica_service.search_music(field, value)

@router.get("/exportar/zip")
def exportar_musics_csv(background_tasks: BackgroundTasks):
    zip_path = musica_service.export_musics_as_zip()

    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    background_tasks.add_task(remove_file, zip_path)

    return FileResponse(
        path=zip_path,
        filename='musics_export.zip',
        media_type='application/zip'
    )

@router.get("/visualizar/hash")
def get_musics_csv_hash():
    return {"hash": musica_service.get_musics_csv_hash()}

@router.get("/exportar/xml")
def exportar_musics_xml(background_tasks: BackgroundTasks):
    xml_path = musica_service.export_musics_as_xml()

    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    background_tasks.add_task(remove_file, xml_path)

    return FileResponse(
        path=xml_path,
        filename='musics_export.xml',
        media_type='application/xml'
    )

@router.get("/{music_id}")
def get_music_by_id(music_id: int):
    music = musica_service.get_music_by_id(music_id)
    return music

@router.post("/")
def create_music(music: MusicaCreate):
    return musica_service.create_music(music)

@router.put("/{music_id}")
def update_music(music_id: int, music: MusicaCreate):
    success = musica_service.update_music(music_id, music)
    return {"message": "Música atualizada com sucesso"}

@router.delete("/{music_id}")
def delete_music(music_id: int):
    success = musica_service.delete_music(music_id)
    return {"message": "Música excluída com sucesso"}
