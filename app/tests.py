import os 
import unittest
import tempfile
from models import *
from flask import * 
#om flask import Flask
#from sqlalchemy.orm import sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)


class AppDBTestCases(unittest.TestCase):


	#def test(self):
		#return True

	'''
	def test_artist_select_1(self):
		artist = Artist.query.filter_by(id='3TVXtAsR1Inumwj472S9r4').first()
		self.assertEqual(artist.name,"Drake")
	def test_album_select_1(self):
		album = Album.query.filter_by(id='2eSzVxzsdcAJal6U6WqTVB').first()
		self.assertEqual(album.name,"Closer (Jauz Remix)")
	def test_track_select_1(self):
		track = Track.query.filter_by(id='2rizacJSyD9S1IQUxUxnsK').first()
		self.assertEqual(track.name,"All We Know")
		def test_artist_insert_1(self):
				db.session.add(Artist(id='1',name='bob'))
				db.session.commit()
				artist = db.session.query(Artist).get('1')
				self.assertEqual(artist.name,"bob")
	'''

		def test_artist_select_1(self):
				artist = Artist.query.filter_by(id='3TVXtAsR1Inumwj472S9r4').first()
				self.assertEqual(artist.name,"Drake")
		def test_album_select_1(self):
				album = Album.query.filter_by(id='2eSzVxzsdcAJal6U6WqTVB').first()
				self.assertEqual(album.name,"Closer (Jauz Remix)")
		def test_track_select_1(self):
				track = Track.query.filter_by(id='2rizacJSyD9S1IQUxUxnsK').first()
				self.assertEqual(track.name,"All We Know")
		def test_artist_insert_1(self):
				db.session.add(Artist(id='1',name='bob'))
				db.session.commit()
				artist = db.session.query(Artist).get('1')
				self.assertEqual(artist.name,"bob")


	# def setUp(self):
	# 	self.db_fd, app.config['DATABASAE'] = tempfile.mkstemp()
	# 	app.config['TESTING'] = True
	# 	self.app = app.test_client()
	# 	with app.app_context():
	# 		app.init_db()

	# def tearDown(self):
	# 	os.close(self.db_fd)
	# 	os.unlink(app.config['DATABASE'])


	# Empty database
	# def test_empty_db(self):
	# 	rv = self.app.get('/')
	# 	assert b'No entries here so far' in rv.data


	# # Insert artists
	# def test_artist_insert_01(self): 
	# 	artists_repr = {"id": "1", "name":"Justin", "genres":"pop","url":"http://artistpage", "followers":"1000", "popularity":"10","image_url":"http://artistimage"}
	# 	a = Artists(**artists_repr)
	# 	self.session.add(a)

	# 	r = self.session.query(Artists).filter(Artists.id == "1").first()
	# 	self.assertEqual(r.name,"Justin")
	# 	self.assertEqual(r.genres,"pop")
	# 	self.assertEqual(r.url, "http://artistpage")
	# 	self.assertEqual(r.followers, "1000")
	# 	self.assertEqual(r.popularity, "10")
	# 	self.assertEqual(r.image_url, "http://artistimage")

	# #Delete Artist
	# def test_artist_delete_01(self): 
	# 	artists_repr = {"id": "1", "name":"Justin", "genres":"pop","url":"http://artistpage", "followers":"1000", "popularity":"10","image_url":"http://artistimage"}
	# 	a = Artists(**artists_repr)
	# 	self.session.add(a)
	# 	r = self.session.query(Artists).filter(Artists.id == "1").first()
	# 	self.assertEqual(r.name,"Justin")

	# 	self.session.delete(a)
	# 	self.session.commit()

	# 	s = self.session.query(Arists.filter(Artists.id == "1".first()))
	# 	self.assertNotEqual(r.name, s.name)


	# # Insert Albums
	# def test_album_insert_01(self): 
	# 	albums_repr = {"id": "1", "name":"Drake Album 1", "url":"http://albumURL","main_artist": "Drake", "main_artist_id":"1",
	# 		       "all_artists":["Drake","Justin"],"type":"Hip-hop","image_url":"http://albumimage"}
	# 	a = Albums(**albums_repr)
	# 	self.session.add(a)

	# 	r = self.session.query(Albums).filter(Albums.id == "1").first()
	# 	self.assertEqual(r.name,"Drake Album 1")
	# 	self.assertEqual(r.url,"http://albumURL")
	# 	self.assertEqual(r.main_artist[0],"Drake")
	# 	self.assertEqual(r.main_artist_id[0], "1")
	# 	self.assertEqual(r.all_artists[1], "Justin")
	# 	self.assertEqual(r.type, "Hip-hop")
	# 	self.assertEqual(r.image_url, "http://albumimage")

	# # Delete Album
	# def test_album_delete_01(self): 
	# 	albums_repr = {"id": "1", "name":"Drake Album 1", "url":"http://albumURL","main_artist": "Drake", "main_artist_id":"1",
	# 		       "all_artists":["Drake","Justin"],"type":"Hip-hop","image_url":"http://albumimage"}
	# 	a = Albums(**albums_repr)
	# 	self.session.add(a)
	# 	r = self.session.query(Albums).filter(Albums.id == "1").first()
	# 	self.assertEqual(r.name,"Drake Album 1")

	# 	self.session.delete(a)
	# 	self.session.commit()

	# 	s = self.session.query(Albums.filter(Albums.id == "1".first()))
	# 	self.assertNotEqual(r.name, s.name)


	# # Insert Tracks
	# def test_track_insert_01(self): 
	# 	tracks_repr = {"id": "1", "name":"Sunshine In My Pocket", "main_artist":"Justin","main_artist_id":"2", "all_artists": ["Justin", "Rhianna"],
	# 		       "track_no":"1", "album_id":"10","duration":3.28, "explicit":false, "popularity":99,
	# 		       "preview_url":"http://preview_url","direct_url":"http://directUrl","image_url":"http://image_url"}
	# 	a = Tracks(**tracks_repr)
	# 	self.session.add(a)

	# 	r = self.session.query(Tracks).filter(Tracks.id == "1").first()
	# 	self.assertEqual(r.name,"Sunshine In My Pocket")
	# 	self.assertEqual(r.main_artist_id, "2")
	# 	self.assertEqual(r.all_artists[1], "Rhianna")
	# 	self.assertEqual(r.track_no, "1")
	# 	self.assertEqual(r.album_id,"10")
	# 	self.assertEqual(r.duration, 3.28)
	# 	self.assertEqual(r.explicit, false)
	# 	self.assertEqual(r.popularity, 99)
	# 	self.assertEqual(r.preview_url, "http://preview_url")
	# 	self.assertEqual(r.direct_url, "http://direct_url")		
	# 	self.assertEqual(r.image_url, "http://image_url")

	# # Delete Track
	# def test_track_delete_01(self): 
	# 	tracks_repr = {"id": "1", "name":"Sunshine In My Pocket", "main_artist":"Justin","main_artist_id":"2", "all_artists": ["Justin", "Rhianna"],
	# 		       "track_no":"1", "album_id":"10","duration":3.28, "explicit":false, "popularity":99,
	# 		       "preview_url":"http://preview_url","direct_url":"http://directUrl","image_url":"http://image_url"}
	# 	a = Tracks(**tracks_repr)
	# 	self.session.add(a)
	# 	r = self.session.query(Tracks).filter(Tracks.id == "1").first()
	# 	self.assertEqual(r.name,"Sunshine In My Pocket")

	# 	self.session.delete(a)
	# 	self.session.commit()

	# 	s = self.session.query(Tracks.filter(Tracks.id == "1".first()))
	# 	self.assertNotEqual(r.name, s.name)



if __name__ == '__main__':
	app.config["TESTING"] = True
	#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_TEST')
	db.create_all()
	unittest.main()
	db.drop_all()
