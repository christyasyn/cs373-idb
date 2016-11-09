from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db, cache
from flask import send_file, jsonify, render_template, make_response
#from sqlalchemy_searchable import parse_search_query, search
from sqlalchemy import func
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
	s = 'Drake'
#	artists = Artist.query.search(s.lower())
	artists = Artist.query.filter(func.lower(s) == func.lower(Artist.name)).all()
	
	print(str(len(artists)))
#	print(artists[0].to_list())
#	print(json.dumps(album_data))



@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
@cache.cached(timeout=600)
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
@cache.cached(timeout=300)
def get_tracks():
#	tracks = Track.query.all()
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
@cache.cached(timeout=300)
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
	album_data["columnDefs"] = [{
		"targets": [0],
		"visible": FALSE,
		"searchable": FALSE
	}]
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

@app.route('/search/<string:search>', methods=['GET'])
@app.route('/search', methods=['GET'])
def return_search(search=None):
	
	# albums = Album.query.filter(func.lower(search) == func.lower(Album.name)).all()
	# album_data = {}
	# album_data['aaData'] = [album.to_list() for album in albums]
	# album_data['columns'] = [
	# 	{ "title": "ID" },
	# 	{ "title": "Album"},
	# 	{ "title": "Main Artist"},
	# 	{ "title": "All Artists"}
	# ]
	# album_data["columnDefs"] = [{
	# 	"targets": [0],
	# 	"visible": FALSE,
	# 	"searchable": FALSE
	# }]
	# album_data['scrollY'] = "500px"
	# album_data['paging'] = "true"

	# tracks = db.session.query(Track, Artist, Album).filter(func.lower(search) == func.lower(Track.name)).filter(Track.album_id == Album.id).filter(Track.main_artist_id == Artist.id).order_by(Track.popularity.desc()).all()
	# tracks_data = []
	# for entry in tracks:
	# 	row = [entry.Track.id, entry.Track.name, str(entry.Track.track_no), entry.Album.name, entry.Artist.name, entry.Track.duration, str(entry.Track.explicit), str(entry.Track.popularity)]
	# 	tracks_data.append(row)
	# track_data = {}
	# track_data['aaData'] = tracks_data
	# track_data['columns'] = [
	# 	{ "title": "ID"},
	# 	{ "title": "Track" },
 #        { "title": "Number" },
 #        { "title": "Album" },
 #        { "title": "Artist" },
 #        { "title": "Duration" },
 #        { "title": "Explicit" },
 #        { "title": "Popularity" }
	# ]
	# track_data["columnDefs"] = [{
	# "targets": [0],
	# "visible": FALSE,
	# "searchable": FALSE
	# }]
	# track_data['scrollY'] = "500px"
	# track_data['paging'] = "true"

	template_stuff = {
		"artists": json.dumps(search_artist(search)),
		"tracks": json.dumps(search_track(search)),
		"albums": json.dumps(search_album(search))
	}
	#return render_template('test.html', test_output=search)
	return render_template('search.html', **template_stuff)

@app.route('/run_unittests')
def run_tests():
	import subprocess
	from os import path
	p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
	output = subprocess.Popen('. /var/www/cs373-idb/app/venv/bin/activate && python3 ' + p, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
	print(output)
	return render_template('test.html', test_output=str(output))


#--------------
# helpers
#--------------

def search_artist(search):
	split_search = search.split()
	artists = Artist.query.filter(func.lower(Artist.name).contains(search)).all()
	artists_data = []
	for artist in artists:
		genres = artist.genres.replace('{', '').replace('}', '').replace('\"', '')
		artists_data.append([artist.id, artist.name, genres, str(artist.followers), str(artist.popularity)])

	for partial in split_search:
		artists = Artist.query.filter(func.lower(Artist.name).contains(partial)).all()
		for artist in artists:
			found = False	
			for item in artists_data:
				if item[0] == artist.id:
					found = True
					break
			if found == False:
				genres = artist.genres.replace('{', '').replace('}', '').replace('\"', '')
				artists_data.append([artist.id, artist.name, genres, str(artist.followers), str(artist.popularity)])

	artist_data = {}
	artist_data["aaData"] = artists_data
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

	return artist_data

def search_album(search):
	search_split = search.split()
	
	albums = Album.query.filter(func.lower(Album.name).contains(search)).all()
	albums_data = []
	for album in albums:
		albums_data.append(album.to_list())

	for partial in search_split:
		albums = Album.query.filter(func.lower(Album.name).contains(partial)).all()
		for album in albums:
			found = False	
			for item in albums_data:
				if item[0] == album.id:
					found = True
					break
			if found == False:
				albums_data.append(album.to_list())

	album_data = {}
	album_data['aaData'] = albums_data
	album_data['columns'] = [
		{ "title": "ID" },
		{ "title": "Album"},
		{ "title": "Main Artist"},
		{ "title": "All Artists"}
	]
	album_data["columnDefs"] = [{
		"targets": [0],
		"visible": FALSE,
		"searchable": FALSE
	}]
	album_data['scrollY'] = "500px"
	album_data['paging'] = "true"

	return album_data

def search_track(search):
	search_split = search.split()
	tracks = db.session.query(Track, Artist, Album).filter(func.lower(Track.name).contains(func.lower(search))).filter(Track.album_id == Album.id).filter(Track.main_artist_id == Artist.id).order_by(Track.popularity.desc()).all()
	tracks_data = []
	for entry in tracks:
		row = [entry.Track.id, entry.Track.name, str(entry.Track.track_no), entry.Album.name, entry.Artist.name, entry.Track.duration, str(entry.Track.explicit), str(entry.Track.popularity)]
		tracks_data.append(row)

	for partial in search_split:
		tracks = db.session.query(Track, Artist, Album).filter(func.lower(Track.name).contains(func.lower(partial))).filter(Track.album_id == Album.id).filter(Track.main_artist_id == Artist.id).order_by(Track.popularity.desc()).all()
		for entry in tracks:
			found = False	
			for item in tracks_data:
				if item[0] == entry.Track.id:
					found = True
					break
			if found == False:
				row = [entry.Track.id, entry.Track.name, str(entry.Track.track_no), entry.Album.name, entry.Artist.name, entry.Track.duration, str(entry.Track.explicit), str(entry.Track.popularity)]
				tracks_data.append(row)
		
	track_data = {}
	track_data['aaData'] = tracks_data
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

	return track_data






#------------------
# RESTful API stuff
#------------------

@app.route('/api/artist/<string:id>', methods=['GET'])
def api_artist(id=None):
	if id == None:
		"""Return error"""
	artist = Artist.query.filter_by(id=id).first()
	return jsonify({'artist': artist.to_json()})

@app.route('/api/artists/<int:page>', methods=['GET'])
@app.route('/api/artists', methods=['GET'])
def api_artists(page=1):
	query = Artist.query.paginate(page=page, per_page=25)
	artists = query.items
	return jsonify({'artists': [artist.to_json() for artist in artists]})


@app.route('/api/album/<string:id>', methods=['GET'])
def api_album(id=None):
	if id == None:
		"""Return error"""
	album = Album.query.filter_by(id=id).first()
	return jsonify({'album': album.to_json()})

@app.route('/api/albums/<int:page>', methods=['GET'])
@app.route('/api/albums', methods=['GET'])
def api_albums(page=1):
	query = Album.query.paginate(page=page, per_page=25)
	albums = query.items
	return jsonify({'albums': [album.to_json() for album in albums]})

@app.route('/api/track/<string:id>', methods=['GET'])
def api_track(id=None):
	if id == None:
		"""Return error"""
	track = Track.query.filter_by(id=id).first()
	return jsonify({'track': track.to_json()})

@app.route('/api/tracks/<int:page>', methods=['GET'])
@app.route('/api/tracks', methods=['GET'])
def api_tracks(page=1):
	query = Track.query.paginate(page=page, per_page=25)
	tracks = query.items
	return jsonify({'tracks': [track.to_json() for track in tracks]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == "__main__":
	# prelist_test()
	# app.debug = True
	app.run()
