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

artist_data = {}

def prelist_test():
	artists = Artist.query.all()
	global artist_data
	artist_data = {}
	artist_data['aaData'] = [artist.to_list() for artist in artists]
	artist_data['columns'] = [
		{ "title": "Artist" },
		{ "title": "Genre" } ,
		{ "title": "Followers" },
		{ "title": "Popularity" }
		]
	with open('./db/all_artist_query.pickle', 'wb') as out:
		pickle.dump(artist_data, out)
	with open('./db.all_artist_query.txt', 'w') as out:
		out.write(json.dumps(artist_data))
	return artist_data



@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
def get_artists():
	global artist_data
	if len(artist_data) == 0:
		try:
			with open('./db/all_artist_query.pickle', 'rb') as read:
				artist_data = dict(pickle.load(read))
		except:
			artist_data = prelist_test()

	return render_template('test.html', test_output=str(len(artist_data)))
	# return json.dumps({'artists': [artist.to_json() for artist in artists]})
	# return render_template('artists.html', artists=json.dumps(artist_data))


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
	app.run()
