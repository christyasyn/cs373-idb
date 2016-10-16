import urllib3
import requests
import json
import pprint

ARTIST_IDS = []
ARTISTS_LIST = []
ARTIST_ALBUMS = []
ALBUM_TRACKS = {}
pp = pprint.PrettyPrinter(indent=4)


def getids():
	response = requests.get('http://kworb.net/spotify/')
	text = response.text.split()
	global ARTIST_IDS
	global ARTISTS_LIST

	# Pull list of artist ids for spotify
	for r in text:
		if 'href' in r:
			split = r.split('"')
			for s in split:
				if 'artist/' in s:
					ARTIST_IDS += [s[7:-5]]
	print('Number of artists: ' + str(len(ARTIST_IDS)))
	with open('id_list.txt', 'w') as out:
		pprint.pprint(ARTIST_IDS, stream=out)
	# Generate key value pairs for artist to ids [artist:id]
	for ref in ARTIST_IDS:
		response = requests.get('https://api.spotify.com/v1/artists/' + ref)
		data = json.loads(response.text)
		ARTISTS_LIST += [{'artist_id': ref, 'artist_name': data['name'], 'popularity': data['popularity'], 'images': data['images'][0], 'genres': list(data['genres']), 'followers': data['followers']['total']}]
		break
	with open('artist_ids_cache.txt', 'w') as out:
		pprint.pprint(ARTISTS_LIST, stream=out)
	artist_album_dict()


def artist_album_dict():
	global ARTIST_ALBUMS
	# Iterate through artist ids and retrieve all albums listed for the artist
	for a in ARTISTS_LIST:
		artist = a['artist_name']
		ident = a['artist_id']
		# inital request for arts albums
		print('https://api.spotify.com/v1/artists/' + ident + '/albums')
		response = requests.get('https://api.spotify.com/v1/artists/' + ident + '/albums')
		data = json.loads(response.text)
		# continue request for current artist albums until no next page is available
		while True:
			for item in data['items']:
				if "US" in item['available_markets']: #pull albums only
					
					album_request = requests.get(item['href'])
					album_info = json.loads(album_request.text)
					d = {}
					tracks = {}
					for a in album_info['artists']:
						d[a['name']] = a['id']
					ARTIST_ALBUMS +=  [{'main_artist': ident, 'main_artist_id': artist, 'artists': d, 'type': item['type'], 'name': item['name'], 'link': item['external_urls']['spotify'], 'id':item['id']}]

			if data['next'] != None:
				response = requests.get(data['next'])
				data = json.loads(response.text)
			else:
				break
	with open('artist_albums_cache.txt', 'w') as out:
		pprint.pprint(ARTIST_ALBUMS, stream=out)

def album_track_dict():
	pass
	global ALBUM_TRACKS
	for artist, albums in ARTIST_ALBUMS.items():
		for a in albums:
			pass



if __name__ == "__main__":
	getids()