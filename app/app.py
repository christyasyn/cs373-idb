from models import Artist, Album, Track
#from sqlalchemy_searchable import parse_search_query, search
from loader import app, db
from flask import send_file

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
	request = Artist.query.paginate()
	artists = request.items
	print (artists)
	return jsonify({'artists': [artists.to_json() for artist in artists] })


if __name__ == "__main__":
	get_artists()
	app.run()
