#!user/bin/env python3
"""
Models.py file that contains all of the 
database models.
"""
from loader import db
from flask.ext.sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy

#dup of above, will delete soon
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String
#from sqlalchemy import Sequence
#from sqlalchemy.orm import sessionmaker



def CreateTables():

	Artists()
	Albums()
	Tracks()

def populateData(): 

	artist = Artist(id=11, name='Prince', followers = 23238947, popularity = 4.9)
	session.add(artist)


# -------------------
# @Artists
# -------------------
class Artist(db.Model):
    """    
    Model for Artists Database
    """
    __tablename__ = 'artists'
    id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    url = db.Column(db.String)
    followers = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    image_url = db.Column(db.String)

    def to_json(self): 
        json_artist = {
            'id' : self.id,
            'name' : self.name,
            'genres' : self.genres,
            'url' : self.url,
            'followers' : self.followers,
            'popularity' : self.popularity,
            'image_url' : self.image_url
        }
    def __repr__(self):
        return 'Artist %r' % self.name

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    main_artists = db.Column(db.String)
    main_artists_id = db.Column(db.String(22))
    all_artists = db.Column(db.String)
    type = db.Column(db.String)
    image_url = db.Column(db.String)

    def to_json(self): 
        json_albums = {
            'id' : self.id,
            'name' : self.name,
            'url' : self.url,
            'main_artists' : self.main_artists,
            'main_artists_id' : self.main_artists_id,
            'all_artists' : self.all_artists,
            'type' : self.db.Column,
            'image_url' : self.image_url
        }

    def __repr__(self):
        return 'Album %r' % self.name

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String)
    main_artists_id = db.Column(db.String(22))
    all_artists = db.Column(db.String)
    track_no = db.Column(db.Integer)
    album_id = db.Column(db.String)
    duration = db.Column(db.String)
    explicit = db.Column(db.Boolean)
    popularity = db.Column(db.Integer)
    preview_url = db.Column(db.String)
    direct_url = db.Column(db.String)
    image_url = db.Column(db.String)

    def to_json(self): 
        json_albums = {
            'id' : self.id,
            'name' : self.name,
            'main_artists_id' : self.main_artists_id,
            'all_artists' : self.all_artists,
            'track_no' : self.track_no,
            'album_id' : self.album_id,
            'duration' : self.duration,
            'explicit' : self.explicit,
            'popularity' : self.popularity,
            'preview_url' : self.preview_url,
            'direct_url' : self.direct_url,
            'image_url' : self.image_url
        }

    def __repr__(self):
        return 'Track %r' % self.name



if __name__ == "__main__":
	createTables()
	populateData()
