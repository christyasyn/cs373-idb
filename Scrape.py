import urllib3
import requests
import json
import pprint

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
		ARTISTS_LIST += [{'artist_id': ref, 
						  'artist_name': data['name'], 
						  'popularity': data['popularity'], 
						  'image': data['images'][0] if len(data['images']) > 0 else [], 
						  'genres': list(data['genres']), 
						  'followers': data['followers']['total'],
						  'direct_url': data['external_urls']['spotify']}]
		# break
	with open('artist_ids_cache.txt', 'w') as out:
		pprint.pprint(ARTISTS_LIST, stream=out)
	artist_album_list()


def artist_album_list():
	global ARTIST_ALBUMS
	# Iterate through artist ids and retrieve all albums listed for the artist
	artist_count = 1
	for a in ARTISTS_LIST:
		artist = a['artist_name']
		ident = a['artist_id']
		# inital request for arts albums
		print('https://api.spotify.com/v1/artists/' + ident + '/albums' + '		' + str(artist_count))
		response = requests.get('https://api.spotify.com/v1/artists/' + ident + '/albums')
		data = json.loads(response.text)
		# continue request for current artist albums until no next page is available
		artist_count += 1 #count for reference use only
		while True:
			for item in data['items']:
				if "US" in item['available_markets']: #pull albums only
					
					print(item['href'])
					# pull individual album info
					album_request = requests.get(item['href'])
					album_info = json.loads(album_request.text)
					d = {}
					tracks = {}
					for a in album_info['artists']:
						d[a['name']] = a['id']
					image = []
					if len(item['images']) > 0:
						image = item['images'][0]
					ARTIST_ALBUMS +=  [{'main_artist': ident, 
										'main_artist_id': artist, 
										'all_artists': d, 
										'type': item['type'], 
										'name': item['name'], 
										'link': item['external_urls']['spotify'], 
										'id':item['id'], 
										'image': image}]
					album_track_list(ident, item['id'], album_info)
					break
			if data['next'] != None:
				response = requests.get(data['next'])
				data = json.loads(response.text)
			else:
				break
	with open('artist_albums_cache.txt', 'w') as out:
		pprint.pprint(ARTIST_ALBUMS, stream=out)
	with open('album_tracks_cache.txt', 'w') as out:
		pprint.pprint(ALBUM_TRACKS, stream=out)

# build list of tracks: track_id, artist_id, album_id, track_number, name, preview_url, direct_url, explicit, image, popularity
def album_track_list(artist_id, album_id, album_info):
	global ALBUM_TRACKS
	tracks = album_info['tracks']['items']
	for items in tracks:
		track_request = requests.get(items['href'])
		track_info = json.loads(track_request.text)
		duration = str((track_info['duration_ms']//1000)//60) + ':' + str((track_info['duration_ms']//1000)%60)
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
		

	
	



if __name__ == "__main__":
	getids()