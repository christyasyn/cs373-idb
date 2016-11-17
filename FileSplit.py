#!/usr/bin/python
import sys
import pickle
import pprint


def split_list(l, new_name):
	open_list = ''
	with open('./app/db/' + l, 'rb') as read:
		open_list = list(pickle.load(read))

	list_1 = open_list[0:len(open_list)//2]
	list_2 = open_list[len(open_list)//2:]

	with open('./app/db/' + new_name + '_1.pickle', 'wb') as out:
		pickle.dump(list_1, out)

	with open('./app/db/' + new_name + '_2.pickle', 'wb') as out:
		pickle.dump(list_2, out)

	with open("./app/db/" + new_name + "_1.txt", 'w') as out:
		pprint.pprint(list_1, stream=out)

	with open("./app/db/" + new_name + "_2.txt", 'w') as out:
		pprint.pprint(list_2, stream=out)

def check_progress(cache_file):
	open_file = ''
	with open('./app/db/' + cache_file, 'rb') as read:
		open_file = list(pickle.load(read))

	pprint.pprint(open_file)

