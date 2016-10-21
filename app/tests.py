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
		artists_repr = {"id": "1", "name":"Justin", "genres":"pop","url": "url", "followers":"followers", "popularity":"10","image_url":"image_url"}
		a = Artists(**artists_repr)
		self.session.add(a)

		r = self.session.query(Artists).filter(Artists.id == "1").first()
		self.assertEqual(r.name,"Justin")
		self.assertEqual(r.genres,"pop")

	# Insert Albums
	def test_albums_insert_01(self): 
		albums_repr = {"id": "1", "name":"Justin", "url":"url","main_artists": "Drake", "main_artists_id":"1",
						 "all_artists":["Drake","Justin"],"type":"type","image_url":"image_url"}
		a = Albums(**albums_repr)
		self.session.add(a)

		r = self.session.query(Albums).filter(Albums.id == "1").first()
		self.assertEqual(r.name,"Justin")
		self.assertEqual(r.main_artists,"Drake")

	# Insert artists
	def test_tracks_insert_01(self): 
		tracks_repr = {"id": "1", "name":"Justin", "main_artists":"Justin","all_artists": ["Drake","Justin"],
						"track_no":"1", "album_id":"10","duration":"3", "explicit":false, "popularity":99,
						"preview_url":"url","direct_url":"dirUrl","image_url":"image_url"}
		a = Tracks(**tracks_repr)
		self.session.add(a)

		r = self.session.query(Tracks).filter(Tracks.id == "1").first()
		self.assertEqual(r.name,"Justin")
		self.assertEqual(r.album_id,"10")




if __name__ = '__main__': 
	unitest.main()