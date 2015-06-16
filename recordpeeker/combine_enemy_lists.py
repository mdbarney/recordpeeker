import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
from collections import OrderedDict, defaultdict

# def combine_enemy_lists_no_duplicates():
# 	path = str(os.getcwd()) + "/enemy_data/"
# 	enemy_file = open("enemy.json", 'w')

# 	data = {}
# 	for dir_entry in os.listdir(path):
# 	    dir_entry_path = os.path.join(path, dir_entry)
# 	    if os.path.isfile(dir_entry_path):
# 	        with open(dir_entry_path, 'r') as my_file:
# 	            # data[dir_entry] = my_file.read()
# 	            data[dir_entry] = json.loads(my_file.read())

#     temp = {}


# 	print >> enemy_file, str(json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)).replace(".json", "")
# 	enemy_file.close()

# {
#                 "ai_id": "1",
#                 "child_pos_id": "1",
#                 "drop_item_list": [
#                     {
#                         "item_id": "40000011",
#                         "num": "1",
#                         "rarity": "1",
#                         "type": 51,
#                         "uid": 201
#                     }
#                 ],
#                 "enemy_id": "304025",
                

def check_for_duplicates(enemy_list, enemy):

	for en in enemy_list:
		if en["enemy_id"] == enemy["enemy_id"]:
			if len(enemy["drop_item_list"]) > 0:
				for item in enemy["drop_item_list"]:
					if item["item_id"] != enemy["enemy_id"]["item_id"]:
						en["drop_item_list"].append(enemy["drop_item_list"])
				
		else:
			en.append(enemy)
	print enemy_list
	return enemy_list


def get_enemy_info():
	enemy_file = os.getcwd() + "/enemy_data/304015.json"

	# data = []
	temp = []
	with open(enemy_file, 'r') as f:
		data = json.loads(f.read())

	# combine the two lists
	for enemy in data:
		for param in enemy["children"]:
			if param["enemy_id"] == enemy["children"]["enemy_id"]:
				if len(param["drop_item_list"]) > 0:
					print len(param["drop_item_list"])
					for item in enemy["children"]["drop_item_list"]:
						if item["item_id"] != enemy["children"]["enemy_id"]["item_id"]:
							en["drop_item_list"].append(enemy["children"]["drop_item_list"])
				
			else:
				temp.append(param)

	return temp

def combine_enemy_lists():
	path = str(os.getcwd()) + "/enemy_data/"
	enemy_file = open("enemy.json", 'w')

	# data = {}
	data = []
	for dir_entry in os.listdir(path):
	    dir_entry_path = os.path.join(path, dir_entry)
	    if os.path.isfile(dir_entry_path):
	        with open(dir_entry_path, 'r') as my_file:
	            # data[dir_entry] = my_file.read()
	            data[dir_entry] = json.loads(my_file.read())
	# print data

	# print >> enemy_file, str(json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)).replace(".json", "")
	enemy_file.close()

def main():
	# combine_enemy_lists()
	print get_enemy_info()

main()