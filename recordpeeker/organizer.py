import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
from collections import OrderedDict, defaultdict

def get_buddy_info(data):
    # use with party_list
    for buddy in data["buddies"]:
        temp_str = buddy.get("name", "Unknown")
        level = buddy.get("level","Unknown")
        job_name = buddy.get("job_name", "Unknown")

        # Tyro check
        if job_name == "Keeper":
            buddy["name"] = "Tyro"

        a = temp_str.replace(" ", "_").lower()

        

        if not os.access(os.getcwd() + "/data/buddy/" + a + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/buddy/" + a + "/")

        if not os.access(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/")

        test_file = open(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/" + a + "_level_" + str(level) + "_stats.json",'w')
        print >> test_file, json.dumps(buddy, indent=4, sort_keys=True)
        test_file.close()

def get_soul_strike_info(data):
    #use with get battle init 
    battle = data["battle"]
    for buddy in battle["buddy"]:
        a = buddy.get("ability_id","Error")
        if not os.access(os.getcwd() + "/data/soul_strike/" + str(a) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/soul_strike/" + str(a) + "/")

        test_file = open(os.getcwd() + "/data/soul_strike/" + str(a) + "/" + str(a) + ".json",'w')
        print >> test_file, json.dumps(buddy.get("soul_strike","Error"), indent=4, sort_keys=True)
        test_file.close()

def get_drop_list(enemy):
	drop_list = []
	for child in enemy["children"]:
		for drops in child["drop_item_list"]:
			drop_list.append(drops)

	return drop_list

def no_duplicates(data, enemy_id):
	
	for enemy in data:
		if enemy["id"] == enemy_id:
			return False
	return True

def uniq(input):
	output = []
	for x in input:
		if x not in output:
			output.append(x)
	return output

def get_ability_info(path):
	enemy_file = os.getcwd() + "/" + path

	temp = []
	with open(enemy_file, 'r') as f:
		data = json.loads(f.read())

	temp = uniq(data)

	return temp

def print_list_to_file(data, path):

	file_path = os.getcwd() + "/" + path 
	test_file = open(file_path, 'w')
	print >> test_file, json.dumps(data, indent=4, sort_keys=True)
	test_file.close()


def get_enemy_info():
	enemy_file = os.getcwd() + "/enemy_data/304015.json"

	# data = []
	temp = []
	temp2 = []
	seen = []
	temp_drop = []
	with open(enemy_file, 'r') as f:
		data = json.loads(f.read())


	# for a in data:
	# 	temp.append(a)

	for enemy in data:
		oid = enemy["id"]
		if len(seen) == 0:
			seen.append(enemy)
		# elif oid is in seen:
		elif no_duplicates(seen, oid):
			seen.append(enemy)
		elif no_duplicates(seen, oid) == False:
			for child in enemy["children"]:
				for drop in child["drop_item_list"]:
					if drop:
						if drop.get("item_id") not in temp_drop:
							temp_drop.append(drop)

	a = uniq(temp_drop)						
	print a
	# return seen

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
	# enemy in data - first bracket (start of dict)
	# child in enemy["children"] - array of children dicts
	# drops in child["drop_item_list"] - array of drop dicts
	# data = []
	party_path = os.path.join(os.getcwd(),"data/raw/handle_party_list/")
	for dir_entry in os.listdir(party_path):
	    dir_entry_path = os.path.join(party_path, dir_entry)
	    if os.path.isfile(dir_entry_path):
	        with open(dir_entry_path, 'r') as my_file:
	            # data[dir_entry] = my_file.read()
	            data = json.loads(my_file.read())
	            get_buddy_info(data)

	# with open(party_path, 'r') as f:
	# 	data = json.loads(f.read())
	# get_buddy_info

	# combine_enemy_lists()
	# temp = get_enemy_info()
	# temp2 = get_ability_info("data/abilities.json")
	# print_list_to_file(temp2, "data/abilities_no_duplicates.json")
	# print temp

	# for i in temp:
	# 	print i["id"]
	
# {u'item_id': u'40000011', u'num': u'1', u'type': 51, u'uid': 201, u'rarity': u'1'}
# {u'item_id': u'40000011', u'num': u'1', u'type': 51, u'uid': 202, u'rarity': u'1'}
# {u'item_id': u'40000011', u'num': u'1', u'type': 51, u'uid': 201, u'rarity': u'1'}

	# a = [{'a': 123}, {'a': 1234}, {'a': 123}, {'a': 12345}]
	# b = []
	# i = int(0)
	# j = int(0)
	# k = int(0)
	# b.append(a[i])
	# while(i < len(a)):
	# 	j = int(0)
	# 	# is_duplicate = False
			
	# 	while(j < len(b)):
	# 		if a[i].get("a") != b[j].get("a"):
	# 			# is_duplicate = True
	# 			b.append(a[i])

	# 		j = j + 1
	# 	# if is_duplicate == False:
	# 	# 	b.append(a[i])
	# 	i = i + 1
	# 	# if a[i] not in a[i+1]:
	# 		# b.append(a[i])

	# # for i in range(0, len(a)):
	# # 	if a[i] not in a[i+1]:
	# # 		b.append(a[i])
	# print a
	# print b

main()