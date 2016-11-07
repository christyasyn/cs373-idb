from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db, cache
from flask import send_file, jsonify, render_template
import json
import pickle
import sys
#-----------
# view pages
#-----------

TRUE = True
FALSE = False

# artist_data = {}



def prelist_test():
	artists = db.session.query(Artist).order_by(Artist.popularity.desc()).all()
	entry = artists[0]
	print(entry.genres.replace('{', '').replace('}', '').replace('\"', ''))
	print('the query did a thing')



@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
@cache.cached(timeout=60)
def get_artists():
#	artists = Artist.query.all()
	artists = db.session.query(Artist).order_by(Artist.popularity.desc()).all()
	data = []
	for artist in artists:
		genres = artist.genres.replace('{', '').replace('}', '').replace('\"', '')
		data.append([artist.id, artist.name, genres, str(artist.followers), str(artist.popularity)])
	artist_data = {}
	artist_data["aaData"] = data
	artist_data["columns"] = [
		{ "title": "ID"},
		{ "title": "Artist" },
		{ "title": "Genre" } ,
		{ "title": "Followers" },
		{ "title": "Popularity" }
		]
	artist_data["columnDefs"] = [{
		"targets": [0],
		"visible": FALSE,
		"searchable": FALSE
		}]
	artist_data['scrollY'] = "500px"
	artist_data['paging'] = "true"
	return render_template('artists.html', artists=json.dumps(artist_data))

@app.route('/tracks', methods=['GET'])
@cache.cached(timeout=60)
def get_tracks():
	#tracks = Track.query.all()
	tracks = db.session.query(Track, Artist, Album).filter(Track.album_id == Album.id).filter(Track.main_artist_id == Artist.id).order_by(Track.popularity.desc()).all()
	data = []
	for entry in tracks:
		row = [entry.Track.id, entry.Track.name, str(entry.Track.track_no), entry.Album.name, entry.Artist.name, entry.Track.duration, str(entry.Track.explicit), str(entry.Track.popularity)]
		data.append(row)
	track_data = {}
	track_data['aaData'] = data
	track_data['columns'] = [
		{ "title": "ID"},
		{ "title": "Track" },
        { "title": "Number" },
        { "title": "Album" },
        { "title": "Artist" },
        { "title": "Duration" },
        { "title": "Explicit" },
        { "title": "Popularity" }
	]
	track_data["columnDefs"] = [{
	"targets": [0],
	"visible": FALSE,
	"searchable": FALSE
	}]
	track_data['scrollY'] = "500px"
	track_data['paging'] = "true"
	return render_template('tracks.html', tracks=json.dumps(track_data))

@app.route('/albums', methods=['GET'])
def get_albums():
	albums = Album.query.all()
	album_data = {}
	album_data['aaData'] = [album.to_list() for album in albums]
	album_data['columns'] = [
		{ "title": "ID" },
		{ "title": "Album"},
		{ "title": "Main Artist"},
		{ "title": "All Artists"}
	]
	album_data["columnDefs"] = [
		{"targets": [0],
		"visible": FALSE,
		"searchable": FALSE},
		{"targets": [1],
		"width": "40%"},
		{"className": "dt-center",
		"targets": "_all"}
	]
	album_data['scrollY'] = "500px"
	album_data['paging'] = "true"
	return render_template('albums.html', albums=json.dumps(album_data))

@app.route('/artist/<string:id>', methods=['GET'])
def single_artist(id):
	artist = Artist.query.filter_by(id=id).first()

	albums = Album.query.filter(Album.main_artists_id==id).all()
	album_data = {"aaData": [], "columns":[{"title": "ID"},{"title": "Album"}, {"title": "Tracks"}, {"title": "Duration"}]}
	album_data["columnDefs"] = [{
		"targets": [0],
		"visible": FALSE,
		"searchable": FALSE
	}]
	album_data['scrollY'] = "500px"
	album_data['paging'] = "true"
	for album in albums:
		album_data["aaData"].append([album.id,album.name, "add later", "add later"])

	template_stuff = {
		"artist_img": artist.image_url,
		"artist_genres": artist.genres,
		"artist_followers": artist.followers,
		"artist_popularity": artist.popularity,
		"artist_name": artist.name,
		"albums": json.dumps(album_data)
	}
	return render_template('artist.html', **template_stuff)

@app.route('/track/<string:id>', methods=['GET'])
def single_track(id):
	track = Track.query.filter_by(id=id).first()

	artist_name = Artist.query.filter_by(id=track.main_artist_id).first()

	album_name = Album.query.filter_by(id=track.album_id).first()

	template_stuff = {
		"track_name": track.name,
		"track_duration": track.duration,
		"track_explicit": track.explicit,
		"track_number": track.track_no,
		"track_popularity": track.popularity,
		"artist_id": artist_name.id,
		"artist_name": artist_name.name,
		"album_id": album_name.id,
		"album_name": album_name.name
	}

	return render_template('track.html', **template_stuff)

@app.route('/album/<string:id>', methods=['GET'])
def single_album(id):
	album = Album.query.filter_by(id=id).first()

	tracks = Track.query.filter_by(album_id=id).all()

	track_data = {"aaData": [], "columns":[{"title": "ID"},{"title": "#"}, {"title": "Title"}, {"title": "Duration"}]}
	track_data["columnDefs"] = [{
		"targets": [0],
		"visible": FALSE,
		"searchable": FALSE
	}]
	track_data['scrollY'] = "500px"
	track_data['paging'] = "true"
	for track in tracks:
		track_data['aaData'].append([track.id,track.track_no, track.name, track.duration])

	template_stuff = {
		"album_img": album.image_url,
		"album_name": album.name,
		"artist_name": album.main_artists,
		"artist_id": album.main_artists_id,
		"additional_artists": album.get_all_artists,
		"number_of_tracks": "add later",
		"tracks": json.dumps(track_data)
	}

	return render_template('album.html', **template_stuff)

@app.route('/about', methods=['GET'])
def get_about():
	return render_template('about.html')

@app.route('/run_unittests', methods=['GET'])
def run_tests():
	import subprocess
	from os import path
	p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
	output = subprocess.Popen('. /var/www/cs373-idb/app/venv/bin/activate && python3 /var/www/cs373-idb/app/tests.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
	print(output)
	return render_template('unittests.html', output=str(output))

if __name__ == "__main__":
	prelist_test()
	app.debug = True
	app.run()
