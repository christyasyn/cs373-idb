import os 
import app
import unittest
import tempfile
from flask import Flask

app = Flask(__name__)
db = SQLAchemy(app)


class AppDBTestCases(unittest.TestCase):

	def setUp(self):
		self.db_fd, app.app.config['DATABASAE'] = tempfile.mkstemp()
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		with app.app.app_context():
			app.inti_db()

	def tearDown(self):
		os.close(self.db_fd)
			os.unlink(app.app.config['DATABASAE'])


	# Empty database
	def test_empty_db(self):
		rv = self.app.get('/')
		assert b'No entries here so far' in rv.data


	# Insert artists
	def test_artists_insert_01(self): 
		artists_repr = {"id": "1", "name":"Justin", "genres":"pop","url":"http://artistpage", "followers":"1000", "popularity":"10","image_url":"http://artistimage"}
		a = Artists(**artists_repr)
		self.session.add(a)

		r = self.session.query(Artists).filter(Artists.id == "1").first()
		self.assertEqual(r.name,"Justin")
		self.assertEqual(r.genres,"pop")
		self.assertEqual(r.url, "http://artistpage")
		self.assertEqual(r.followers, "1000")
		self.assertEqual(r.popularity, "10")
		self.assertEqual(r.image_url, "http://artistimage")


	# Insert Albums
	def test_albums_insert_01(self): 
		albums_repr = {"id": "1", "name":"Drake Album 1", "url":"http://albumURL","main_artist": "Drake", "main_artist_id":"1",
						 "all_artists":["Drake","Justin"],"type":"Hip-hop","image_url":"http://albumimage"}
		a = Albums(**albums_repr)
		self.session.add(a)

		r = self.session.query(Albums).filter(Albums.id == "1").first()
		self.assertEqual(r.name,"Drake Album 1")
		self.assertEqual(r.url,"http://albumURL")
		self.assertEqual(r.main_artist[0],"Drake")
		self.assertEqual(r.main_artist_id[0], "1")
		self.assertEqual(r.all_artists[1], "Justin")
		self.assertEqual(r.type, "Hip-hop")
		self.assertEqual(r.image_url, "http://albumimage")


	# Insert artists
	def test_tracks_insert_01(self): 
		tracks_repr = {"id": "1", "name":"Sunshine In My Pocket", "main_artist":"Justin","main_artist_id":"2", "all_artists": ["Justin", "Rhianna"],
						"track_no":"1", "album_id":"10","duration":3.28, "explicit":false, "popularity":99,
						"preview_url":"http://preview_url","direct_url":"http://dirUrl","image_url":"http://image_url"}
		a = Tracks(**tracks_repr)
		self.session.add(a)

		r = self.session.query(Tracks).filter(Tracks.id == "1").first()
		self.assertEqual(r.name,"Sunshine In My Pocket")
		self.assertEqual(r.main_artist_id, "2")
		self.assertEqual(r.all_artists[1] = "Rhianna")
		self.assertEqual(r.track_no, "1")
		self.assertEqual(r.album_id,"10")
		self.assertEqual(r.duration, 3.28)
		self.assertEqual(r.explicit, false)
		self.assertEqual(r.popularity, 99)
		self.assertEqual(r.preview_url, )
		self.assertEqual(r.direct_url, )		
		self.assertEqual(r.image_url, )


if __name__ = '__main__': 
	unitest.main()