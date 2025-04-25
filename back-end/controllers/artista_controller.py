from services import artista_service
from fastapi import APIRouter, HTTPException
from models.artista_model import ArtistaCreate

router = APIRouter()

@router.get("/")
def get_all_artists():
  return artista_service.get_all_artists()


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