import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
from collections import OrderedDict, defaultdict

def combine_enemy_lists():
	path = str(os.getcwd()) + "/enemy_data/"
	enemy_file = open("enemy.json", 'w')

	data = {}
	for dir_entry in os.listdir(path):
	    dir_entry_path = os.path.join(path, dir_entry)
	    if os.path.isfile(dir_entry_path):
	        with open(dir_entry_path, 'r') as my_file:
	            # data[dir_entry] = my_file.read()
	            data[dir_entry] = json.loads(my_file.read())

	print >> enemy_file, str(json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)).replace(".json", "")
	enemy_file.close()

def main():
	combine_enemy_lists()

main()