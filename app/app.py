from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db
from flask import send_file, jsonify, render_template
import json
#-----------
# view pages
#-----------


artist_data = {}

def prelist_test():
        global artist_data
        artists = Artist.query.all()
        artist_data['aaData'] = [artist.to_list() for artist in artists]
        artist_data['columns'] = [
              { "title": "Artist" },
              { "title": "Genre" } ,
              { "title": "Followers" },
              { "title": "Popularity" }
             ]

@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
def get_artists():
	prelist_test()
	# return json.dumps({'artists': [artist.to_json() for artist in artists]})
	return render_template('artists.html', artists=jsonify(artist_data))


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
