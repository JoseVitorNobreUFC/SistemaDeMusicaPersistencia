from services import album_service
from fastapi import APIRouter, HTTPException
from models.album_model import AlbumCreate

router = APIRouter()

@router.get("/")
def get_all_albums():
  return album_service.get_all_albums()


@router.get("/{album_id}")
def get_album_by_id(album_id: int):
  return album_service.get_album_by_id(album_id)


@router.post("/")
def create_album(album: AlbumCreate):
  return album_service.create_album(album)


@router.put("/{album_id}")
def update_album(album_id: int, album: AlbumCreate):
  return album_service.update_album(album_id, album)


@router.delete("/{album_id}")
def delete_album(album_id: int):
  return album_service.delete_album(album_id)