from utils.generic_crud import (
  get_all_records,
  get_record_by_id,
  create_record,
  update_record,
  delete_record
)
from models.artista_model import Artista

AUTHOR_CSV_PATH = './data/artists.csv'

def get_all_artists():
  return get_all_records(AUTHOR_CSV_PATH)

def get_artist_by_id(artist_id):
  return get_record_by_id(AUTHOR_CSV_PATH, artist_id)

def create_artist(artist):
  return create_record(AUTHOR_CSV_PATH, artist)

def update_artist(artist_id, artist):
  return update_record(AUTHOR_CSV_PATH, artist_id, artist)

def delete_artist(artist_id):
  return delete_record(AUTHOR_CSV_PATH, artist_id)

