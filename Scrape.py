
#!/usr/bin/python
import urllib3
import requests
import json
import pprint
import pickle
import threading
import multiprocessing
import time

ARTIST_IDS = []
ARTISTS_LIST = []
ARTIST_ALBUMS = []
ALBUM_TRACKS = []
pp = pprint.PrettyPrinter(indent=4)
lock = multiprocessing.Lock()


class album_list_exception(Exception):
	'''This is the exception for the main album list not being available'''

def getids(artist_list):
	response = requests.get(artist_list)
	text = response.text.split()
	global ARTIST_IDS
	global ARTISTS_LIST
	temp_list = []

	# Pull list of artist ids for spotify
	count = 1
	for r in text:
		if 'href' in r:
			split = r.split('"')
			for s in split:
				if 'artist/' in s:
					print(count)
					response = requests.get('https://api.spotify.com/v1/artists/' + s[7:-5])
					data = json.loads(response.text)
					ARTISTS_LIST += [{'id': s[7:-5], 
						  'name': data['name'], 
						  'popularity': data['popularity'], 
						  'image': data['images'][0] if len(data['images']) > 0 else [], 
						  'genres': list(data['genres']), 
						  'followers': data['followers']['total'],
						  'direct_url': data['external_urls']['spotify']}]
					count += 1
	# verify number of artists included in list						  
	print('Number of artists: ' + str(len(ARTISTS_LIST)))
	# save pickle file with artists info
	with open('./app/db/artist_ids_cache.pickle', 'wb') as out:
		pickle.dump(ARTISTS_LIST, out)
	# save readable artist info
	with open('./app/db/artist_ids_cache.txt', 'w') as out:
		pprint.pprint(ARTISTS_LIST, stream=out)


def start_album_populate():
	# if artist list is empty, read in artists from file.
	global ARTISTS_LIST
	if len(ARTISTS_LIST) == 0:
		with open('./app/db/artist_ids_cache.pickle', 'rb') as read:
			ARTISTS_LIST = list(pickle.load(read))

	# access global album list		
	global ARTIST_ALBUMS
	# Iterate through artist ids and retrieve all albums listed for the artist
	print(len(ARTISTS_LIST))
	threads = []
	for i in range(0, len(ARTISTS_LIST)):
		while threading.active_count() > 4:
			"""do some stuff"""
		# if i % 5 == 0:
		# 	for t in threads:
		# 		t.join()
		thread = threading.Thread(target=artist_album_list, args=(ARTISTS_LIST[i], i + 1))
		threads.append(thread)
		thread.start()

	# save file of album basic info
	with open('./app/db/artist_albums_cache.pickle', 'wb') as out:
		pickle.dump(ARTIST_ALBUMS, out)
	with open('./app/db/artist_albums_cache.txt', 'w') as out:
		pprint.pprint(ARTIST_ALBUMS, stream=out)


def artist_album_list(a, artist_num):

	global ARTIST_ALBUMS
	# print(str(artist_count))
	artist = a['name']
	ident = a['id']
	print('Starting: ' + '{0: <25}'.format(artist) + '		' + str(artist_num))
	# inital request for arts albums
	# print(artist + '		' + str(artist_count))
	lock.acquire()
	while True:
		try:
			response = requests.get('https://api.spotify.com/v1/artists/' + ident + '/albums')
			data = json.loads(response.text)
			if 'items' in data:
				# print(artist + ' first request')
				break
			else:
				print('initial: ' + str(response.status_code))
				raise album_list_exception
		except :
			print("Album List retrieval error, retrying: " + str(data.status_code))
			continue

	lock.release()
	# continue request for current artist albums until no next page is available
	while True:
		for item in data['items']:
			if "US" in item['available_markets']: #pull albums only
				
				# pull individual album info
				lock.acquire()
				while True:
					album_request = requests.get(item['href'])
					album_info = json.loads(album_request.text)
					if 'name' not in album_info:
						print(artist + ': ' + str(album_request.status_code))
						continue
					else:
						break
				lock.release()
				# print(album_info['name'])
				d = {}
				tracks = {}
				for a in album_info['artists']:
					d[a['name']] = a['id']
				image = []
				if len(item['images']) > 0:
					image = item['images'][0]
				lock.acquire()
				# print(artist + ': ' + album_info['name'])
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
				lock.release()
		if data['next'] != None:
			lock.acquire()
			while True:
				temp_data = data
				response = requests.get(data['next'])
				data = json.loads(response.text)
				if 'items' not in data:
					print(artist + ': ' + response.status_code)
					data = temp_data
					continue
				else:
					break
			lock.release()
		else:
			break
	print(artist +  ' complete')
	# except:	
	# 	# print(data)
	# 	print('Retreival error: ' + str(response.status_code))
	# 	artist_album_list(a)
	# finally:
	# 	pass



def start_track_populate():
	global ARTIST_ALBUMS
	if len(ARTIST_ALBUMS) == 0:
		with open('./app/db/artist_albums_cache.pickle', 'rb') as read:
			ARTIST_ALBUMS = pickle.load(read)

	t0 = time.time()
	album_count = 1
	threads = []
	pool = multiprocessing.Pool(processes=4)

	for i in range(0, len(ARTIST_ALBUMS)):
		if i % 3 == 0:
			for t in threads:
				t.join()
			threads = []
		p = threading.Thread(target=album_track_process, args=(ARTIST_ALBUMS[i]['main_artist_id'], ARTIST_ALBUMS[i]['id'], ARTIST_ALBUMS[i]['main_artist'], ARTIST_ALBUMS[i]['name'], i))
		threads.append(p)
		p.start()

	for t in threads:
		t.join()

	t1 = time.time()
	total_time = t1 - t0
	print(str(total_time))

	# save artist album list
	with open('./app/db/artist_albums_cache.pickle', 'wb') as out:
		pickle.dump(ARTIST_ALBUMS, out)
	with open('./app/db/artist_albums_cache.txt', 'w') as out: 
		pprint.pprint(ARTIST_ALBUMS, stream=out)

	# save tracks list
	with open('./app/db/album_tracks_cache.pickle', 'wb') as out:
		pickle.dump(ALBUM_TRACKS, out)
	with open('./app/db/album_tracks_cache.txt', 'w') as out:
		pprint.pprint(ALBUM_TRACKS, stream=out)


# build list of tracks: track_id, artist_id, album_id, track_number, name, preview_url, direct_url, explicit, image, popularity
def album_track_list(artist_id, album_id, artist, album_name):
	global ALBUM_TRACKS
	album_duration = 0

	response = requests.get('https://api.spotify.com/v1/albums/' + album_id + '/tracks')
	tracks = json.loads(response.text)

	for items in tracks['items']:
		track_request = requests.get(items['href'])
		track_info = json.loads(track_request.text)
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


def album_track_process(artist_id, album_id, artist, album_name, album_list_number):
	global ALBUM_TRACKS
	global ARTIST_ALBUMS
	album_duration = 0

	lock.acquire()
	response = requests.get('https://api.spotify.com/v1/albums/' + album_id + '/tracks')
	tracks = json.loads(response.text)
	lock.release()

	try:
		for items in tracks['items']:
			track_request = requests.get(items['href'])
			track_info = json.loads(track_request.text)
			duration = str((track_info['duration_ms']//1000)//60) + ':' + str('{0:03d}'.format((track_info['duration_ms']//1000)%60))
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
			lock.acquire()
			ALBUM_TRACKS += [track_list_entry]
			lock.release()
		print(str(album_list_number))
	except:
		print('Restarting: ' + str(album_list_number) + ': ' + response)
		album_track_process(artist_id, album_id, artist, album_name, album_list_number)
	finally:
		pass

def verify_tracks():
	global ALBUM_TRACKS
	if len(ALBUM_TRACKS) == 0:
		with open('./app/db/album_tracks_cache.pickle', 'rb') as read:
			ALBUM_TRACKS = pickle.load(read)
	global ARTISTS_LIST
	if len(ARTISTS_LIST) == 0:
		with open('./app/db/artist_ids_cache.pickle', 'rb') as read:
			ARTISTS_LIST = pickle.load(read)
	global ARTIST_ALBUMS
	if len(ARTIST_ALBUMS) == 0:
		with open('./app/db/artist_albums_cache.pickle', 'rb') as read:
			ARTIST_ALBUMS = pickle.load(read)

	for track in ALBUM_TRACKS:
		artist = ''
		for a in ARTISTS_LIST:
			if a['id'] == track['artist_id']:
				artist = a['name']
				break
		album = ''
		for a in ARTIST_ALBUMS:
			if a['id'] == track['album_id']:
				album = a['name']
		print('{:30.25} {:30.25} {:30.25} {:30.25} {:30.25}'.format(track['track_id'], artist, album, track['name'], track['duration']))





# def populate_tracks():
# 	if len(artist_ids_cache) == 0:
# 		try:
