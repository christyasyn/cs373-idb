from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db
from flask import send_file, jsonify, render_template
import json
#-----------
# view pages
#-----------



@app.route('/sanity', methods=['GET'])
def sanity():
	return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route("/artists", methods=['GET'])
def get_artists():
	# artists  = Artist.query.all()
	# artists = {'artists': [artists[i].to_json() for i in range(0, 10)]}
	# artists['columns'] = [
 #              { "title": "Artist" },
 #              { "title": "Genre" } ,
 #              { "title": "Followers" },
 #              { "title": "Popularity" }
 #             ]
	artists = {"artists":[
		["Drake", "canadian pop", "6856957", "100"],
		["Justing Bieber", "canadian pop", "6548382", "97"]
		],
		"columns": [
			{ "title": "Artist" },
			{ "title": "Genre" } ,
			{ "title": "Followers" },
			{ "title": "Popularity" }
			]}
	#artists = request.items
	# return json.dumps({'artists': [artist.to_json() for artist in artists]})
	return render_template('artists.html', artists=jsonify(artists))


@app.route('/run_unittests')
def run_tests():
	from subprocess import getoutput
	from os import path
	p = path.join(path.dirname(path.realpath(__file__)), 'tests.py')
	output = getoutput('python '+p)
	print(output)
	return jsonify({'output': str(output)})

if __name__ == "__main__":
	app.run(debug=True)
