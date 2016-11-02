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
	tracks = Track.query.all()
	track_data = {}
	track_data['aaData'] = [track.to_list() for track in tracks]
	track_data['colums'] = [
		{ "title": "Track" },
        { "title": "Number" },
        { "title": "Album" },
        { "title": "Artist" },
        { "title": "Duration" },
        { "title": "Explicit" },
        { "title": "Popularity" }
	]
	print(json.dumps(track_data))



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
def get_albums():
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


@app.route('/run_unittests')
def run_tests():
	from subprocess import getoutput
	from os import path
	p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
	output = getoutput('python '+p)
	print(output)
	return jsonify({'output': str(output)})

if __name__ == "__main__":
	prelist_test()
	app.debug = True
	app.run()
