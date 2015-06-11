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

def calc_atk_damage():
	# If ATK ≤ 346, then Damage = (ATK)1.8 ÷ √(DEF)
	# If ATK > 346, then Damage = 2000 • √(ATK) ÷ √(DEF)

def calc_chance_to_hit():
# The base accuracy of an attack is equal to the following:
# (base chance to hit) + Acc * 8/35 - Eva * 6/35
# where base chance to hit = 90, thus:
# 90 + Acc * 8/35 - Eva * 6/35 

# Things to note:
# 	1. This only applies to physical attacks.
# 	2. This chance is then capped between 20% and 100% inclusively.
# 	3. When blinded, your Acc is decreased by 50% (before the calculation).
# 		This occurs after your hit rate is capped at 100% but before the 20% min cap



def calc_healing_power():

# Healing spells like Curaga and Prayer use a fairly simple formula with very few additional modifiers. 
# The base formula to determine the amount that is healed is as follows:
# Power * (5 + (Mnd^0.75) * 100 / 256)
 
# This is rounded to the nearest integer value. The baseline Power value for Cure is 30. This means 
# that for someone with 150 Mnd, the amount healed with Cure would be: 
# 30 * (5 + (1500.75) * 100 / 256) = 30 * (5 + 42.86 * 100 / 256) = 30 * 21.74 = 652.28 = 652



def main():
	combine_enemy_lists()

main()






# # test.py
# def combine_enemy_lists():
# 	path = str(os.getcwd()) + "/data/"
# 	enemy_file = open("enemy.json", 'w')

# 	data = {}
# 	for dir_entry in os.listdir(path):
# 	    dir_entry_path = os.path.join(path, dir_entry)
# 	    if os.path.isfile(dir_entry_path):
# 	        with open(dir_entry_path, 'r') as my_file:
# 	            # data[dir_entry] = my_file.read()
# 	            data[dir_entry] = json.loads(my_file.read())

# 	print >> enemy_file, str(json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)).replace(".json", "")
# 	enemy_file.close()

# def csv_write_magic(data):
# 	# temp.append([dungeon_id, series_id, id, name, difficulty, type, rounds, stamina, has_boss])
#     data.insert(0, ["dungeon_id", "series_id", "id", "name", "difficulty", "type", "rounds", "stamina", "has_boss"])
    
#     with open('test.tsv', 'wb') as f:
#         writer = csv.writer(f, delimiter='\t',quoting=csv.QUOTE_NONE)
#         writer.writerows(data)
#         # writer.writerow(data)

# def csv_read_magic():
# 	# # temp.append([dungeon_id, series_id, id, name, difficulty, type, rounds, stamina, has_boss])
# 	# with open('test.tsv', 'rb') as f:
# 	#     writer = csv.writer(f, delimiter='\t',quoting=csv.QUOTE_NONE)
# 	#     writer.writerows(data)
# 	#     # writer.writerow(data)

# 	temp = []
# 	with open('test.tsv', 'rb') as f:
# 		a = csv.reader(f, delimiter='\t', quotechar='"')
# 		for row in a:
# 			print '\t'.join(row)

# def main():
# 	temp = []
# 	temp.append([620068, 106001, 720214, "Ebonfist Keep - Heroic, Part 1", 80, "NORMAL", 3, 15, 0])
# 	temp.append([620068, 106001, 720215, "Ebonfist Keep - Heroic, Part 2", 80, "NORMAL", 3, 15, 0])
# 	temp.append([620068, 106001, 720216, "Ebonfist Keep - Heroic, Part 3", 80, "NORMAL", 3, 15, 0])
# 	temp.append([620070, 106001, 720220, "Gil Greenwood - Normal, Part 1", 23, "NORMAL", 3, 5, 0])
# 	temp.append([620070, 106001, 720221, "Gil Greenwood - Normal, Part 2", 23, "NORMAL", 3, 5, 0])
# 	temp.append([620070, 106001, 720222, "Gil Greenwood - Normal, Part 3", 23, "NORMAL", 3, 5, 0])
	
# 	# combine_enemy_lists()
# 	csv_write_magic(temp)
# 	# csv_read_magic()

# main()
