from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db
from flask import send_file, jsonify
import json
#-----------
# view pages
#-----------



@app.route('/sanity', methods=['GET'])
def sanity():
	return "This is a sanity check!"

@app.route('/index.html', methods=['GET'])
def index_exp():
	return send_file('index.html')


@app.route('/', methods=['GET'])
def index():
	return send_file('index.html')

@app.route('/api/artists', methods=['GET'])
def get_artists():
	artists  = Artist.query.all()
	#artists = request.items
	return json.dumps({'artists': [artist.to_json() for artist in artists]})


if __name__ == "__main__":
	artist_list = get_artists()
	print (artist_list)
	app.run()
