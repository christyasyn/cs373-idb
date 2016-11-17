import os 
import unittest
import tempfile
from models import *
import flask
from app import db, app
from flask_sqlalchemy import SQLAlchemy

class AppDBTestCases(unittest.TestCase):

	def test_artist_select_1(self):
		artist = Artist.query.filter_by(id='3TVXtAsR1Inumwj472S9r4').first()
		self.assertEqual(artist.name,"Drake")
	def test_album_select_1(self):
		album = Album.query.filter_by(id='5iCP6JeHtNV66LnfCKoFF1').first()
		self.assertEqual(album.name,"Jason Derulo Special Edition EP")
	def test_track_select_1(self):
		track = Track.query.filter_by(id='2rizacJSyD9S1IQUxUxnsK').first()
		self.assertEqual(track.name,"All We Know")

	def test_artist_select_2(self):
		artist = Artist.query.filter_by(name='Drake').first()
		self.assertEqual(artist.id,"3TVXtAsR1Inumwj472S9r4")
	def test_album_select_2(self):
		album = Album.query.filter_by(name='Y.U. MAD').first()
		self.assertEqual(album.id,"1wHsOxEWMUAEsAHk9Q3Yz7")
	def test_track_select_2(self):
		track = Track.query.filter_by(name='All We Know').first()
		self.assertEqual(track.id,"4dSFpcFAtXQD6MGZWVddhk")


	def test_artist_select_none(self):
		artist = Artist.query.filter_by(id='5').first()
		self.assertEqual(artist,None)
	def test_album_select_none(self):
		album = Album.query.filter_by(id='5').first()
		self.assertEqual(album,None)
	def test_track_select_none(self):
		track = Track.query.filter_by(id='5').first()
		self.assertEqual(track,None)

	def test_artist_insert_1(self):
		artist = Artist(id='1',name='bob', popularity=1, image_url='url', genres='pop', followers=2, url='url')
		db.session.add(artist)
		db.session.commit()
		artist = Artist.query.filter_by(id='1').first()
		self.assertEqual(artist.name,"bob")


	def test_artist_delete_1(self):
			a = Artist.query.filter_by(id = "1").first()
			self.assertEqual(a.name, 'bob')
			db.session.delete(a)
			db.session.commit()
			a = Artist.query.filter_by(id = "1").first()
			self.assertEqual(a, None)

	def test_album_insert_1(self):
		album = Album(id='1',name='bob', url='url', main_artist='main_artist', main_artist_id='artist id', all_artists='all artists', type='type', image_url='image url', release_date=None, popularity=50, record_label='Columbia', duration='2', number_of_tracks='1')
		db.session.add(album)
		db.session.commit()
		album = Album.query.filter_by(id='1').first()
		self.assertEqual(album.name,"bob")


	def test_album_delete_1(self):
			a = Album.query.filter_by(id = "1").first()
			self.assertEqual(a.name, 'bob')
			db.session.delete(a)
			db.session.commit()
			a = Album.query.filter_by(id = "1").first()
			self.assertEqual(a, None)

	def test_track_insert_1(self):
		track = Track(id='1',name='bob', direct_url='url', main_artist_id='main_artist', all_artists='all artists', duration='dur', explicit=True, popularity=10,preview_url='url',track_no=1,album_id='1')
		db.session.add(track)
		db.session.commit()
		track = Track.query.filter_by(id='1').first()
		self.assertEqual(track.name,"bob")


	def test_track_delete_1(self):
			a = Track.query.filter_by(id = "1").first()
			self.assertEqual(a.name, 'bob')
			db.session.delete(a)
			db.session.commit()
			a = Track.query.filter_by(id = "1").first()
			self.assertEqual(a, None)

	def test_artist_insert_2(self):
		artist = Artist(id='2',name='bob', popularity=1, image_url='url', genres='pop', followers=2, url='url')
		db.session.add(artist)
		db.session.commit()
		artist = Artist.query.filter_by(id='2').first()
		self.assertEqual(artist.name,"bob")


	def test_artist_delete_2(self):
		a = Artist.query.filter_by(id = "2").first()
		self.assertEqual(a.name, 'bob')
		db.session.delete(a)
		db.session.commit()
		a = Artist.query.filter_by(id = "2").first()
		self.assertEqual(a, None)

	def test_album_insert_2(self):
		album = Album(id='2',name='bob', url='url', main_artist='main_artist', main_artist_id='artist id', all_artists='all artists', type='type', image_url='image url')
		db.session.add(album)
		db.session.commit()
		album = Album.query.filter_by(id='2').first()
		self.assertEqual(album.name,"bob")


	def test_album_delete_2(self):
		a = Album.query.filter_by(id = "2").first()
		self.assertEqual(a.name, 'bob')
		db.session.delete(a)
		db.session.commit()
		a = Album.query.filter_by(id = "2").first()
		self.assertEqual(a, None)

	def test_track_insert_2(self):
		track = Track(id='2',name='bob', direct_url='url', main_artist_id='main_artist', all_artists='all artists', duration='dur', explicit=True, popularity=10,preview_url='url',track_no=1,album_id='1')
		db.session.add(track)
		db.session.commit()
		track = Track.query.filter_by(id='2').first()
		self.assertEqual(track.name,"bob")


	def test_track_delete_2(self):
		a = Track.query.filter_by(id = "2").first()
		self.assertEqual(a.name, 'bob')
		db.session.delete(a)
		db.session.commit()
		a = Track.query.filter_by(id = "2").first()
		self.assertEqual(a, None)


	# def setUp(self):
	# 	self.db_fd, app.config['DATABASAE'] = tempfile.mkstemp()
	# 	app.config['TESTING'] = True
	# 	self.app = app.test_client()
	# 	with app.app_context():
	# 		app.init_db()

	# def tearDown(self):
	# 	os.close(self.db_fd)
	# 	os.unlink(app.config['DATABASE'])


	# # Empty database
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

	#Delete Artist
	# def test_artist_delete_01(self): 
	# 	artists_repr = {"id": "1", "name":"Justin", "genres":"pop","url":"http://artistpage", "followers":"1000", "popularity":"10","image_url":"http://artistimage"}
	# 	a = Artists(**artists_repr)
	# 	db.session.add(a)
	# 	r = db.session.query(Artists).filter(Artists.id == "1").first()
	# 	self.assertEqual(r.name,"Justin")

	# 	db.session.delete(a)
	# 	db.session.commit()

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
