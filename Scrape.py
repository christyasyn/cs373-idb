
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

	# open progress log if available
	start_point = 0
	try:
		with open('./app/db/album_progress.txt', 'r') as f:
			start_point = int(f.readline().rstrip())
	except:
		pass

	if len(ARTISTS_LIST) == start_point:
		return
	# access global album list		
	global ARTIST_ALBUMS

	if start_point != 0:
		with open('./app/db/artist_albums_cache.pickle', 'rb') as read:
			ARTIST_ALBUMS = list(pickle.load(read))
	# Iterate through artist ids and retrieve all albums listed for the artist
	print(len(ARTISTS_LIST))
	threads = []
	for i in range(start_point, len(ARTISTS_LIST)):
		while threading.active_count() > 4:
			"""do some stuff"""
		if i % 50 == 0:
			for t in threads:
				t.join()
			with open('./app/db/artist_albums_cache.pickle', 'wb') as out:
				pickle.dump(ARTIST_ALBUMS, out)
			with open('./app/db/artist_albums_cache.txt', 'w') as out:
				pprint.pprint(ARTIST_ALBUMS, stream=out)
			with open('./app/db/album_progress.txt', 'w') as out:
				out.write(str(i))
			print("---------------------Progress Saved---------------------")
		thread = threading.Thread(target=artist_album_list, args=(ARTISTS_LIST[i], i + 1))
		threads.append(thread)
		thread.start()

	# save file of album basic info
	with open('./app/db/artist_albums_cache.pickle', 'wb') as out:
		pickle.dump(ARTIST_ALBUMS, out)
	with open('./app/db/artist_albums_cache.txt', 'w') as out:
		pprint.pprint(ARTIST_ALBUMS, stream=out)
	with open('./app/db/album_progress.txt', 'w') as out:
		out.write(str(len(ARTISTS_LIST)))


def artist_album_list(a, artist_num):

	global ARTIST_ALBUMS
	artist = a['name']
	ident = a['id']
	# print('Starting: ' + '{0: <25}'.format(artist) + '		' + str(artist_num))
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
					d[a['id']] = a['name']
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
									'number_of_tracks': album_info['tracks']['total']},]
				lock.release()
		if data['next'] != None:
			lock.acquire()
			while True:
				temp_data = data
				response = requests.get(data['next'])
				data = json.loads(response.text)
				if 'items' not in data:
					print(artist + ': ' + str(response.status_code))
					data = temp_data
					continue
				else:
					break
			lock.release()
		else:
			break
	# print(artist +  ' complete')


def start_track_populate(album_list, track_progress, cache_file):
	# read in the list of albums to be used
	global ARTIST_ALBUMS
	if len(ARTIST_ALBUMS) == 0:
		with open('./app/db/' + album_list, 'rb') as read:
			ARTIST_ALBUMS = pickle.load(read)

	start_point = 0
	# check for progress of track in album_list
	try:
		with open('./app/db/' + track_progress, 'r') as f:
			start_point = int(f.readline().rstrip())
	except:
		pass
	print(str(len(ARTIST_ALBUMS)))
	print(str(start_point))

	# read in existing cached file
	global ALBUM_TRACKS
	if start_point != 0:
		with open('./app/db/' + cache_file + '.pickle', 'rb') as read:
			ALBUM_TRACKS = list(pickle.load(read))

	t0 = time.time()
	threads = []
	# start iteration through list to fill tracks collection
	for i in range(start_point, len(ARTIST_ALBUMS)):
		# Maintain active thread limit
		while threading.active_count() > 4:
			"""wait for a thread to finish"""
		# Save progress at every 100 albums completed
		if i % 100 == 0:
			for t in threads:
				t.join()
			threads = []
			# save tracks list
			with open('./app/db/' + cache_file + '.pickle', 'wb') as out:
				pickle.dump(ALBUM_TRACKS, out)
			# with open('./app/db/album_tracks_cache.txt', 'w') as out:
			# 	pprint.pprint(ALBUM_TRACKS, stream=out)
			with open('./app/db/' + track_progress, 'w') as out:
				out.write(str(i))
			print('---------------------Progress Saved: ' + str(i) + '---------------------')

		# Start new thread for next album in list	
		p = threading.Thread(target=album_track_process, args=(ARTIST_ALBUMS[i]['main_artist_id'], ARTIST_ALBUMS[i]['id'], ARTIST_ALBUMS[i]['main_artist'], ARTIST_ALBUMS[i]['name'], i))
		threads.append(p)
		p.start()

	for t in threads:
		t.join()

	t1 = time.time()
	total_time = t1 - t0
	print(str(total_time))

	# save tracks list
	with open('./app/db/' + cache_file + '.pickle', 'wb') as out:
		pickle.dump(ALBUM_TRACKS, out)
	with open('./app/db/' + cache_file + '.txt', 'w') as out:
		pprint.pprint(ALBUM_TRACKS, stream=out)


# build list of tracks: track_id, artist_id, album_id, track_number, name, preview_url, direct_url, explicit, image, popularity
def album_track_process(artist_id, album_id, artist, album_name, album_list_number):
	global ALBUM_TRACKS #access global album tracks list
	global ARTIST_ALBUMS # access global artist albums list
	album_duration = 0
	print("Starting: " + '{0: <9}'.format(str(album_list_number)))
	lock.acquire()
	response = requests.get('https://api.spotify.com/v1/albums/' + album_id + '/tracks')
	tracks = json.loads(response.text)
	lock.release()

	try:
		for items in tracks['items']:

			lock.acquire()
			track_request = requests.get(items['href'])
			track_info = json.loads(track_request.text)
			lock.release()

			duration = str((track_info['duration_ms']//1000)//60) + ':' + str('{0:02d}'.format((track_info['duration_ms']//1000)%60))
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
								'duration_ms': track_info['duration_ms'],
								'preview': track_info['preview_url'], 
								'explicit': track_info['explicit'], 
								'direct_url': track_info['external_urls']['spotify'], 
								'popularity': track_info['popularity']}
			lock.acquire()
			ALBUM_TRACKS += [track_list_entry]
			lock.release()
		# print("Completed: " + '{0: <75}'.format(artist['name'] + ' - '+ album_name) + str(album_list_number))
	except:
		# print('Restarting: ' + '{0: <65}'.format(artist['name'] + " - " + album_name) + str(album_list_number) + ': ' + str(response))
		album_track_process(artist_id, album_id, artist, album_name, album_list_number)
	finally:
		pass
