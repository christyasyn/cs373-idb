import os
import json, re
from app import db, app
from models import Artist, Album, Track
from datetime import datetime
import pickle
#from dateutil import parser
import time
import requests

base = '../../db/'

# clear pending commits
db.session.commit()

start_time = time.time()


        
# insert artist rows into table. 
# @param cach_file: the cached file containing the row data for each artist
def load_artists(cache_file):
        with open(os.path.join(base, cache_file), 'rb') as artist_file:
            artist_pickle = pickle.load(artist_file)
            print('artist pickle loaded, good job guys!')
        for a in artist_pickle:
                idd = a['id']
                name = a['name']
                popularity = a['popularity'] 
                if not a['image'] : 
                     image = ''
                else: 
                     image = a['image']['url']
                genres = a['genres']
                followers = a['followers']
                direct_url = a['direct_url']

                artist = Artist(id=idd, name=name, popularity=popularity, image_url=image,
                                genres=genres, followers=followers, url=direct_url)

                db.session.add(artist)
                db.session.commit()
        print ('Artists committed')

# insert album rows into table.
# @param cache_file: cached file containing the row data for each album

def load_albums(cache_file):
        with open(os.path.join(base, cache_file), 'rb') as album_file:
                album_pickle = pickle.load(album_file)
                print('album pickle loaded, good job guys!')
        for a in album_pickle:
                idd = a['id']
                name = a['name']
                if not a['link']:
                    link = ''
                else:
                    link = a['link']
                if not a['image']:
                      image=''
                else:
                      image = a['image']['url']
                main_artist = a['main_artist']
                main_artist_id = a['main_artist_id']
                all_artists = a['all_artists']
                artist_list = []
                for k,v in all_artists.items():
                        artist_list.append (v)       
                album_type = a['type']
                duration = a['duration']
                release_date = a['release_date']
                record_label = a['record_label']
                popularity = a['popularity']
                number_of_tracks = a['number_of_tracks']

                album = Album(id=idd, name=name, url=link, main_artists=main_artist, main_artists_id=main_artist_id, all_artists=artist_list, type=album_type, image_url=image, duration=duration, release_date=release_date, record_label=record_label, popularity=popularity, number_of_tracks=number_of_tracks) 
                r = Album.query.get(idd)
                if not r:
                        db.session.add(album)
                        db.session.commit()
        print ('Albums committed')         

def load_tracks():
        with open(os.path.join(base, 'album_tracks_cache.pickle'), 'rb') as tracks_file:
                tracks_pickle = pickle.load(tracks_file)
                print('tracks pickle loaded, good job guys!')
        for t in tracks_pickle:
                idd = t['track_id']
                name = t['name']
                if not t['direct_url']:
                    link = ''
                else:
                    link = t['direct_url']
                main_artist_id = t['artist_id']
                all_artists = t['all_artists']
                artist_list = []
                for k,v in all_artists.items():
                        artist_list.append (v)       
                duration = t['duration']
                explicit = t['explicit']
                popularity = t['popularity']
                preview = t['preview']
                track_number = t['track_number']
                album_id = t['album_id']
                duration_ms = t['duration_ms']
                track = Track(id=idd, name=name, direct_url=link, main_artist_id=main_artist_id, all_artists=artist_list, duration=duration, explicit=explicit, popularity=popularity, preview_url=preview, track_no=track_number, album_id=album_id, duartion_ms=duraiton_ms)
                r = Track.query.get(idd)
                if not r:
                        db.session.add(track)
                        db.session.commit()
        print ('Tracks committed')         
