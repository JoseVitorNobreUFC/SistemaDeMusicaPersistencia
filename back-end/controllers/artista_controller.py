from services import artista_service
from fastapi import APIRouter, HTTPException
from models.artista_model import Artista

router = APIRouter()

@router.get("/")
def get_all_artists():
  return artista_service.get_all_artists()


@router.get("/{artist_id}")
def get_artist_by_id(artist_id: int):
  return artista_service.get_artist_by_id(artist_id)


@router.post("/")
def create_artist(artist: Artista):
  return artista_service.create_artist(artist)


@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: Artista):
  return artista_service.update_artist(artist_id, artist)


@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
  return artista_service.delete_artist(artist_id)