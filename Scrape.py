
#!/usr/bin/python
import urllib3
import requests
import json
import pprint
import pickle

ARTIST_IDS = []
ARTISTS_LIST = []
ARTIST_ALBUMS = []
ALBUM_TRACKS = []
pp = pprint.PrettyPrinter(indent=4)

def getids():
	response = requests.get('http://kworb.net/spotify/')
	text = response.text.split()
	global ARTIST_IDS
	global ARTISTS_LIST
	temp_list = []

	# Pull list of artist ids for spotify
	for r in text:
		if 'href' in r:
			split = r.split('"')
			for s in split:
				if 'artist/' in s:
					response = requests.get('https://api.spotify.com/v1/artists/' + s[7:-5])
					data = json.loads(response.text)
					ARTISTS_LIST += [{'id': s[7:-5], 
						  'name': data['name'], 
						  'popularity': data['popularity'], 
						  'image': data['images'][0] if len(data['images']) > 0 else [], 
						  'genres': list(data['genres']), 
						  'followers': data['followers']['total'],
						  'direct_url': data['external_urls']['spotify']}]
	# verify number of artists included in list						  
	print('Number of artists: ' + str(len(ARTIST_IDS)))
	# print list of artist ids to file
	with open('id_list.txt', 'w') as out:
		pprint.pprint(ARTIST_IDS, stream=out)
	# save pickle file with artists info
	with open('artist_ids_cache.pickle', 'wb') as out:
		pickle.dump(ARTISTS_LIST, out)
	# save readable artist info
	with open('artist_ids_cache.txt', 'w') as out:
		pprint.pprint(ARTISTS_LIST, stream=out)


def artist_album_list():
	# if artist list is empty, read in artists from file.
	global ARTISTS_LIST
	if len(ARTISTS_LIST) == 0:
		with open('artist_ids_cache.pickle', 'rb') as read:
			ARTISTS_LIST = list(pickle.load(read))

	# access global album list		
	global ARTIST_ALBUMS
	# Iterate through artist ids and retrieve all albums listed for the artist
	print(len(ARTISTS_LIST))
	artist_count = 1
	for a in ARTISTS_LIST:
		print(str(artist_count))
		artist = a['name']
		ident = a['id']
		# inital request for arts albums
		# print(artist + '		' + str(artist_count))
		response = requests.get('https://api.spotify.com/v1/artists/' + ident + '/albums')
		data = json.loads(response.text)
		# continue request for current artist albums until no next page is available
		artist_count += 1 #count for reference use only
		while True:
			for item in data['items']:
				if "US" in item['available_markets']: #pull albums only
					
					# pull individual album info
					album_request = requests.get(item['href'])
					album_info = json.loads(album_request.text)
					# print(album_info['name'])
					d = {}
					tracks = {}
					for a in album_info['artists']:
						d[a['name']] = a['id']
					image = []
					if len(item['images']) > 0:
						image = item['images'][0]
					ARTIST_ALBUMS +=  [{'main_artist': artist, 
										'main_artist_id': ident, 
										'all_artists': d, 
										'type': album_info['type'], 
										'name': album_info['name'], 
										'link': album_info['external_urls']['spotify'], 
										'id':album_info['id'], 
										'image': album_info['images'][0] if len(album_info['images']) > 0 else [],
										'duration': 0,
										'release_date': album_info['release_date'],
										'record_label':album_info['label'],
										'popularity': album_info['popularity'],
										'number_of_tracks': album_info['tracks']['total']}]
			if data['next'] != None:
				response = requests.get(data['next'])
				data = json.loads(response.text)
			else:
				break
	# save file of album basic info
	with open('artist_albums_cache.pickle', 'wb') as out:
		pickle.dump(ARTIST_ALBUMS, out)
	with open('artist_albums_cache.txt', 'w') as out:
		pprint.pprint(ARTIST_ALBUMS, stream=out)

def start_track_populate():
	global ARTIST_ALBUMS
	if len(ARTIST_ALBUMS) == 0:
		with open('artist_albums_cache.pickle', 'rb') as read:
			ARTIST_ALBUMS = pickle.load(read)

	for album in ARTIST_ALBUMS:
		album['duration'] = album_track_list(album['main_artist_id'], album['id'])

	with open('album_tracks_cache.pickle', 'wb') as out:
		pickle.dump(ARTIST_ALBUMS, out)		


# build list of tracks: track_id, artist_id, album_id, track_number, name, preview_url, direct_url, explicit, image, popularity
def album_track_list(artist_id, album_id):

	global ALBUM_TRACKS
	album_duration = 0

	response = requests.get('https://api.spotify.com/v1/albums/' + album_id + '/tracks')
	tracks = json.loads(response.text)

	for items in tracks:
		track_request = requests.get(items['href'])
		track_info = json.loads(track_request.text)
		print(artist + '	', end='')
		print(track_info['name'])
		duration = str((track_info['duration_ms']//1000)//60) + ':' + str((track_info['duration_ms']//1000)%60)
		album_duration += int(track_info['duration_ms'])
		all_artists = {}
		for artist in track_info['artists']:
			all_artists[artist['name']]= artist['id']
		track_list_entry = {'track_id': track_info['id'], 
							'artist_id': artist_id, 
							'all_artists': all_artists,
							'album_id': album_id, 
							'track_number': track_info['track_number'], 
							'name': track_info['name'], 
							'duration': duration, 
							'preview': track_info['preview_url'], 
							'explicit': track_info['explicit'], 
							'direct_url': track_info['external_urls']['spotify'], 
							'popularity': track_info['popularity']}
		ALBUM_TRACKS += [track_list_entry]

	return str((album_duration//1000)//60) + ':' + str((album_duration//1000)%60)

# def populate_tracks():
# 	if len(artist_ids_cache) == 0:
# 		try:


# if __name__ == "__main__":
# 	getids()
# 	# artist_album_list()