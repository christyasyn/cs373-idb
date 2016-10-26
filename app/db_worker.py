import os
import json, re
from app import db, app
from models import Artist, Album, Track
from datetime import datetime
import pickle
#from dateutil import parser
import time
import requests

base = './db'

# clear pending commits
db.session.commit()

start_time = time.time()

with open(os.path.join(base, 'artist_ids_cache.pickle'), 'rb') as artist_file:
        artist_pickle = pickle.load(artist_file)
        print('artist pickle loaded, good job guys!')

with open(os.path.join(base, 'artist_albums_cache.pickle'), 'rb') as album_file:
        album_pickle = pickle.load(album_file)
        print('album pickle loaded, good job guys!')
        
with open(os.path.join(base, 'album_tracks_cache.pickle'), 'rb') as tracks_file:
        tracks_pickle = pickle.load(tracks_file)
        print('tracks pickle loaded, good job guys!')
def load_artists():
        for a in artist_pickle:
                name = a['name']
                popularity = a['popularity']
                image = dict (a['image'])
                image = image ['url']
                genres = a['genres']
                followers = a['followers']
                direct_url = a['direct_url']

                artist = Artist(name=name, popularity=popularity, image_url=image,
                                genres=genres, followers=followers, url=direct_url)

                db.session.add(artist)
        db.session.commit()
        print('artists commited')
