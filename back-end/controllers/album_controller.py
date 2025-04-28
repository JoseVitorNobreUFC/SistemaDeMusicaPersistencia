from services import album_service
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.album_model import AlbumCreate
from fastapi.responses import FileResponse
import os


router = APIRouter()

@router.get("/")
def get_all_albums():
  return album_service.get_all_albums()

@router.get("/exportar")
def exportar_album_csv(background_tasks: BackgroundTasks):
  zip_path = album_service.export_albums_as_zip()

  def remove_file(path: str):
    if os.path.exists(path):
      os.remove(path)

  background_tasks.add_task(remove_file, zip_path)

  return FileResponse(
    path=zip_path,
    filename='albuns_export.zip',
    media_type='application/zip'
  )

@router.get("/hash")
def get_album_csv_hash():
  return {"hash": album_service.get_albums_csv_hash()}

@router.get("/exportar-xml")
def exportar_album_xml(background_tasks: BackgroundTasks):
    xml_path = album_service.export_albums_as_xml()

    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    background_tasks.add_task(remove_file, xml_path)

    return FileResponse(
        path=xml_path,
        filename='albuns_export.xml',
        media_type='application/xml'
    )

@router.get("/{album_id}")
def get_album_by_id(album_id: int):
  album = album_service.get_album_by_id(album_id)
  if not album:
    raise HTTPException(status_code=404, detail="Album nao encontrado")
  return album


@router.post("/")
def create_album(album: AlbumCreate):
  return album_service.create_album(album)


@router.put("/{album_id}")
def update_album(album_id: int, album: AlbumCreate):
  success = album_service.update_album(album_id, album)
  if not success:
    raise HTTPException(status_code=404, detail="Album nao encontrado para atualizacao")
  return {"message": "Album atualizado com sucesso"}

@router.delete("/{album_id}")
def delete_album(album_id: int):
  success = album_service.delete_album(album_id)
  if not success:
    raise HTTPException(status_code=404, detail="Album nao encontrado pra exclusao")
  return {"message": "Album excluido com sucesso"}

