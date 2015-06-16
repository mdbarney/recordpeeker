import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
import math
from collections import OrderedDict, defaultdict

def get_enemy_info():
	enemy_file = os.getcwd() + "/test_enemy.json"

	data = []
	temp = []
	with open(enemy_file, 'r') as f:
		data = json.loads(f.read())

	for child in data["children"]:
		# for param in child["params"]
		temp = child["params"]

	return temp

	# data = {}
	# for dir_entry in os.listdir(path):
	#     dir_entry_path = os.path.join(path, dir_entry)
	#     if os.path.isfile(dir_entry_path):
	#         with open(dir_entry_path, 'r') as my_file:
	#             # data[dir_entry] = my_file.read()
	#             data[dir_entry] = json.loads(my_file.read())

def calculate_damage(user_atk, enemy_def, power_multiplier):

	if user_atk <= 346:
		damage = ((float(user_atk) ** 1.8)/(math.sqrt(float(enemy_def))) * power_multiplier)
	else:#if user_atk > 346:
		damage = (2000.0 * math.sqrt(float(user_atk))/(math.sqrt(float(enemy_def))) * power_multiplier)

	return damage

def atk_to_one_hit_ko(enemy_max_hp, enemy_def, power_multiplier):
	
	# (max hp * sqrt(def))^(1/1.8) = atk
	# (max hp * sqrt(def)/2000)^2 = atk

	atk1 = (enemy_max_hp * math.sqrt(enemy_def)) ** (1/1.8)
	atk2 = ((enemy_max_hp * math.sqrt(enemy_def))/2000) ** 2

	# print "atk1: " + str(atk1)
	# print "atk2: " + str(atk2)

	if atk1 <= 346:
		return int(math.ceil(atk1))
	elif atk2 > 346:
		return int(math.ceil(atk2))
	else:
		return "Not possible"


# def get_abilities(data):
# 	return 


# def get_stat(stat, data, value):
def get_stat(stat, data):
	for param in data:
		# print param.get(stat, -1)
		return param.get(stat, -1)

def print_basic_stats(data):
	print "Name:\t" + get_stat("disp_name", data)
	print "ID:\t" + get_stat("id", data)
	print "HP:\t" + get_stat("max_hp", data)
	print "Level:\t" + get_stat("lv", data)
	print "EXP:\t" + get_stat("exp", data)
	print "acc:\t" + get_stat("acc", data)
	print "atk:\t" + get_stat("atk", data)
	print "def:\t" + get_stat("def", data)
	print "eva:\t" + get_stat("eva", data)
	print "matk:\t" + get_stat("matk", data)
	print "mdef:\t" + get_stat("mdef", data)
	print "mnd:\t" + get_stat("mnd", data)
	print "spd:\t" + get_stat("spd", data)

def main():

	power_multiplier = 1 # used for regular attack

	enemy_info = get_enemy_info()
	# print "Please enter atk value: "
	# atk = raw_input()
	# damage = calculate_damage(atk, get_stat("def",enemy_info), power_multiplier)
	# print "Damage: " + str(math.floor(damage))
	print enemy_info
	# get_max_hp(enemy_info)
	print "atk needed to 1-hit KO enemy: " + str(atk_to_one_hit_ko(get_stat("max_hp",enemy_info), get_stat("def",enemy_info), power_multiplier))
	# print atk_to_one_hit_ko(float(get_stat("max_hp",enemy_info)), float(get_stat("def",enemy_info)), power_multiplier)


main()


# def get_acc(data):
# 	return 

# def get_atk(data):
# 	return data["atk"]

# def get_def(data):
# 	for param in data:
# 		return hp.get("max_hp",999999)

# def get_disp_name(data):
# 	return data["disp_name"]

# def get_eva(data):
# 	return data["eva"]

# def get_exp(data):
# 	return data["exp"]

# def get_id(data):
# 	return data["id"]

# def get_matk(data):
# 	return data["matk"]

# def get_max_hp(data):
# 	for hp in data:
# 		return hp.get("max_hp",999999)

# def get_mdef(data):
# 	return data["mdef"]

# def get_mnd(data):
# 	return data["mnd"]

# def get_spd(data):
# 	return data["spd"]



# "params": [
#                     {
#                         "abilities": [
#                             {
#                                 "ability_id": "201338",
#                                 "weight": "100"
#                             }
#                         ],
#                         "acc": "100",
#                         
#                         "atk": 331,
#                         "breed_id": "4",
#                         "counters": [],
#                         "critical": "3",
#                         "def": 152,
#                         "def_attributes": [
#                             {
#                                 "attribute_id": "220",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "211",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "210",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "101",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "225",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "102",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "221",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "219",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "201",
#                                 "factor": "1"
#                             },
#                             {
#                                 "attribute_id": "222",
#                                 "factor": "1"
#                             }
#                         ],
#                         "disp_name": "Murussu",
#                         "eva": "70",
#                         "exp": 812,
#                         "id": "3100491",
#                         "looking": "0",
#                         "lv": "80",
#                         "matk": 336,
#                         "max_hp": 2733,
#                         "mdef": 148,
#                         "mnd": 229,
#                         "no": "1",
#                         "size": "2",
#                         "spd": "100"
#                     }
#                 ],
