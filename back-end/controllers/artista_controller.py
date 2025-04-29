from services import artista_service
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.artista_model import ArtistaCreate
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/")
def get_all_artists():
  return artista_service.get_all_artists()

@router.get("/exportar")
def exportar_artists_csv(background_tasks: BackgroundTasks):
  zip_path = artista_service.export_artists_as_zip()

  def remove_file(path: str):
    if os.path.exists(path):
      os.remove(path)

  background_tasks.add_task(remove_file, zip_path)

  return FileResponse(
    path=zip_path,
    filename='artists_export.zip',
    media_type='application/zip'
  )

@router.get("/hash")
def get_artists_csv_hash():
  return {"hash": artista_service.get_artists_csv_hash()}

@router.get("/exportar-xml")
def exportar_artists_xml(background_tasks: BackgroundTasks):
    xml_path = artista_service.export_artists_as_xml()

    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    background_tasks.add_task(remove_file, xml_path)

    return FileResponse(
        path=xml_path,
        filename='artists_export.xml',
        media_type='application/xml'
    )


@router.get("/{artist_id}")
def get_artist_by_id(artist_id: int):
  artist = artista_service.get_artist_by_id(artist_id)
  if not artist:
    raise HTTPException(status_code=404, detail="Artista nao encontrado")
  return artist


@router.post("/")
def create_artist(artist: ArtistaCreate):
  return artista_service.create_artist(artist)


@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: ArtistaCreate):
  success = artista_service.update_artist(artist_id, artist)
  if not success:
    raise HTTPException(status_code=404, detail="Artista nao encontrado para atualizacao")
  return artista_service.update_artist(artist_id, artist)


@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
  success = artista_service.delete_artist(artist_id)
  if not success:
    raise HTTPException(status_code=404, detail="Artista nao encontrado para exclusao")
  return artista_service.delete_artist(artist_id)