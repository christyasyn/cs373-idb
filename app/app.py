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
	return "This is a sanity check!"

@app.route('/', methods=['GET'])
def index():
	return send_file('index.html')

@app.route('/#/artists', methods=['GET'])
def get_artists():
	artists  = Artist.query.all()
	artists = {'artists': [artist.to_json() for artist in artists]}
	artists['columns'] = [
              { "title": "Artist" },
              { "title": "Genre" } ,
              { "title": "Followers" },
              { "title": "Popularity" }
             ]
	#artists = request.items
	# return json.dumps({'artists': [artist.to_json() for artist in artists]})
	return render_template('artists.html', artists=artists)


if __name__ == "__main__":
	# artist_list = get_artists()
	# print (artist_list)
	app.run()
