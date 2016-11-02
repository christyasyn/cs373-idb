from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db
from flask import send_file, jsonify, render_template
import json
import pickle
import sys
#-----------
# view pages
#-----------

# artist_data = {}

def prelist_test():
	# albums = Album.query.all()
	# album_data = {}
	# album_data['aaData'] = [albums[0].to_list()]
	# album_data['columns'] = [
	# 	{"title": "Album"},
	# 	{"title": "Main Artist"},
	# 	{"title": "All Artists"}
	#]
	track = Track.query.filter_by(id=id).first()
	print(track)

	artist_name = Artist.query.filter_by(Artist.id == track.main_artist_id).first().name
	print(artist_name)
	print(json.dumps(album_data))



@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
def get_artists():
	artists = Artist.query.all()
	artist_data = {}
	artist_data["aaData"] = [artist.to_list() for artist in artists]
	artist_data["columns"] = [
		{ "title": "Artist" },
		{ "title": "Genre" } ,
		{ "title": "Followers" },
		{ "title": "Popularity" }
		]

	return render_template('artists.html', artists=json.dumps(artist_data))

@app.route('/tracks', methods=['GET'])
def get_tracks():
	tracks = Track.query.all()
	track_data = {}
	track_data['aaData'] = [track.to_list() for track in tracks]
	track_data['columns'] = [
		{ "title": "Track" },
        { "title": "Number" },
        { "title": "Album" },
        { "title": "Artist" },
        { "title": "Duration" },
        { "title": "Explicit" },
        { "title": "Popularity" }
	]
	return render_template('tracks.html', tracks=json.dumps(track_data))

@app.route('/albums', methods=['GET'])
def get_albums():
	albums = Album.query.all()
	album_data = {}
	album_data['aaData'] = [album.to_list() for album in albums]
	album_data['columns'] = [
		{"title": "Album"},
		{"title": "Main Artist"},
		{"title": "All Artists"}
	]

	return render_template('albums.html', albums=json.dumps(album_data))

@app.route('/artist/<string:id>', methods=['GET'])
def single_artist(id):
	artist = Artist.query.filter_by(id=id).first()

	albums = Album.query.filter(Album.main_artists_id==id).all()
	album_data = {"aaData": [], "columns":[{"title": "Album"}, {"title": "Tracks"}, {"title": "Duration"}]}

	for album in albums:
		album_data["aaData"].append([album.name, "add later", "add later"])

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

	artist_name = Artist.query.filter_by(id=track.main_artist_id).first().name

	template_stuff = {
		"track_name": track.name,
		"track_duration": track.duration,
		"track_explicit": track.explicit,
		"track_number": track.track_no,
		"track_popularity": track.popularity,
		"artist_name": artist_name
	}

	return render_template('track.html', **template_stuff)


@app.route('/run_unittests')
def run_tests():
	from subprocess import getoutput
	from os import path
	p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
	output = getoutput('python '+p)
	print(output)
	return jsonify({'output': str(output)})

if __name__ == "__main__":
	#prelist_test()
	app.debug = True
	app.run()
