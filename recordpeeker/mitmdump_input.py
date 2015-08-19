import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
import csv
import time
import datetime
import pprint
import re
import sys
# import wget
from collections import OrderedDict, defaultdict

from libmproxy.protocol.http import decoded
from tabulate import tabulate

from recordpeeker import Equipment, ITEMS, BATTLES, DUNGEONS, slicedict, best_equipment
from recordpeeker.dispatcher import Dispatcher

current_dungeon_id = 0
temp_party_list = []

# TODO
def save_battles(data):
    # temp.append([dungeon_id, series_id, id, name, difficulty, type, rounds, stamina, has_boss])
    # temp = ["dungeon_id", "series_id", "id", "name", "difficulty", "type", "rounds", "stamina", "has_boss"]
    file_path = os.getcwd() + "/data/battle_log.csv"
    if (os.path.isfile(file_path) == False):
        data.insert(0, ["dungeon_id", "series_id", "id", "name", "difficulty", "type", "rounds", "stamina", "has_boss"])
        with open(file_path, 'w') as f:
            writer = csv.writer(f, delimiter='\t',quoting=csv.QUOTE_NONE)
            writer.writerows(data)
    else:
        with open(file_path, 'a') as f:
            writer = csv.writer(f, delimiter='\t',quoting=csv.QUOTE_NONE)
            writer.writerows(data)

def save_single_equipment_by_id(item, path):
    temp = []
    equipment_id = item.get("equipment_id","Error")
    level = item.get("level","0")
    name = item.get("name","Error")
    # name1 = name.replace("\uff0b","+")
    # name1 = name.replace("\xef","")
    utf8_str = name.encode('utf-8')
    name1 = name
    if '\xef' in utf8_str:
        # print str(equipment_id) + " " + utf8_str
        # name1 = utf8_str.replace("\xef","")
        name2 = re.split('\)', name)
        name1 = str(name2[0]) + ")"

    if ITEMS.get(equipment_id,"Not found") == "Not found":
        temp.append([equipment_id, name])
        # save_equipment_id(temp)
        # print name1
        save_equipment_id(equipment_id, name)
        # reload dict ITEMS dict?
        # doesnt work
        # ITEMS = __init__.load_dict("data/items.csv")

    if not os.access(os.getcwd() + path + str(equipment_id) + "/", os.F_OK):
        os.mkdir(os.getcwd() + path + str(equipment_id) + "/")
    
    file_path = os.getcwd() + path + str(equipment_id) + "/" + str(equipment_id) + "_level_" + str(level) + ".json"
    
    ###DEBUG###
    # print os.listdir(os.getcwd() + path + str(equipment_id) + "/")
    
    # if not os.path.isfile(file_path):
    if not os.access(file_path, os.F_OK):
        print "Saved stats for: [" + str(name1) + " (id: " + str(equipment_id) + ") - level " + str(level) + "]"
        test_file = open(file_path,'w')
        print >> test_file, json.dumps(item, indent=4, sort_keys=False)
        test_file.close()

# def save_equipment_id(data):
def save_equipment_id(equipment_id, name):
    # temp.append([dungeon_id, series_id, id, name, difficulty, type, rounds, stamina, has_boss])
    # temp = ["dungeon_id", "series_id", "id", "name", "difficulty", "type", "rounds", "stamina", "has_boss"]
    file_path = os.getcwd() + "/data/items.csv"
    # unicode_str = name.decode('ascii')
    utf8_str = name.encode('utf-8')
    name1 = name
    with open(file_path, 'a') as f:
        # writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_NONE)
        if '\xef' in utf8_str:
            # print str(equipment_id) + " " + utf8_str
            # name1 = utf8_str.replace("\xef","")
            name2 = re.split('\)', name)
            name1 = str(name2[0]) + ")"
        print >> f, str(equipment_id) + "," + str(name1)
        # writer.writerows([[equipment_id,name1]])

def save_character_sprite(path):
    print 1
    ### handle_dungeon_list ###
    ### "/Content/xx/xx/etc" might be run within the app itself
    # assets["assetPath"]: "/Content/lang/bgm/bgm_m4a/bgm_06_006.json"
    ### Serverside ###
    # dungeons["background_image_path"]: "/dff/static/lang/image/dungeon/620075_bg.png"

    # dungeons["background_image_path"]["prizes"]["1"][["image_path"]]: ## seems like only 1-3
    # dungeons["epilogue_image_path"]: "/dff/static/lang/image/dungeon/620075_epilogue.png"
    # dungeons["prologue_image_path"]: "/dff/static/lang/image/dungeon/620075_prologue.png"
    # world["image_path"]: "/dff/static/lang/image/world/800002.png"
    # world["door_image_path"]: "/dff/static/lang/image/world/800002_door.png"

    ### handle_get_battle_init_data ###
    # buddy["weapon"]["path"]: "100002/100002.json"
    # buddy["weapon"]["assets"]:
    # buddy["abilities"]["assets"]:
    # rounds["enemy"]["animation_info"]["assets"]:
    ## pretty much everything with "assets" or assetPath
    # rounds["assets"] (maybe it's just "assets" without rounds)

    ### handle_party_list ###
    # abilities[]
    #   "command_icon_path": "/dff/static/lang/image/ability/30111021/30111021_128.png"
    #   "image_path": "/dff/static/lang/image/ability/30111021/30111021_112.png"
    #   "thumbnail_path": "/dff/static/lang/image/ability/30111021/30111021_48.png"
    # buddies[]
    #   "image_path": "/dff/static/lang/image/buddy/10000200/10000200.png"
    # equipments[]
    #   "detail_image_path": "/dff/static/lang/image/equipment/21001010/21001010_05_220.png"
    #   "image_path": "/dff/static/lang/image/equipment/21001010/21001010_05_112.png"
    #   "thumbnail_path": "/dff/static/lang/image/equipment/21001010/21001010_05_48.png"
    # grow_eggs[]
    #   "image_path": "/dff/static/lang/image/growegg/70000001/70000001_112.png"
    # materials[]
    #   "image_path": "/dff/static/lang/image/ability_material/40000063/40000063_112.png"
    # record_materias[]
    #   "command_icon_path": "/dff/static/lang/image/record_materia/111000020/111000020_128.png", 
    #   "image_path": "/dff/static/lang/image/record_materia/111000020/111000020_112.png", 


    #     filename = wget.download(path)

def get_buddy_info(data):
    # use with party_list
    json_path = "/data/buddy_id/"
    for buddy in data["buddies"]:
        level = buddy.get("level","Unknown")
        job_name = buddy.get("job_name", "Unknown")
        buddy_id = buddy.get("id","0")

        # Tyro name check
        if job_name == "Keeper":
            buddy["name"] = "Tyro"

        temp_str = buddy.get("name", "Unknown")

        if job_name == "Dark Knight" and buddy["name"] == "Cecil":
            temp_str = "CecilDK"

        if job_name == "Paladin" and buddy["name"] == "Cecil":
            temp_str = "CecilP"

        a = temp_str.replace(" ", "_").lower()

        # check if file/folder exist, AKA enter new data
        if not os.access(os.getcwd() + "/data/buddy/" + a + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/buddy/" + a + "/")

        if not os.access(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/")

        test_file_path = os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/" + a + "_level_" + str(level) + "_stats.json"  
        if not os.access(test_file_path, os.F_OK):
            print "Saved stats for: [" + buddy["name"] + " (id: " + str(buddy_id) + ") - level " + str(level) + "]"
            with open(test_file_path, 'w') as f:
                print >> f, json.dumps(buddy, indent=4, sort_keys=False)

        if not os.access(os.getcwd() + json_path + str(buddy_id) + "/", os.F_OK):
            os.mkdir(os.getcwd() + json_path + str(buddy_id) + "/")

        json_file_path = os.getcwd() + json_path + str(buddy_id) + "/" + a + "_level_" + str(level) + "_stats.json"  
        if not os.access(json_file_path, os.F_OK):
            # print "Saved stats for: [" + buddy["name"] + " (id: " + str(buddy_id) + ") - level " + str(level) + "]"
            with open(json_file_path, 'w') as f:
                print >> f, json.dumps(buddy, indent=4, sort_keys=False)

        # ### THIS OVERWRITES ALL BUDDY DATA FOR UPDATED CHARACTERS ###
        # if buddy["name"] == "Cyan" or buddy["name"] == "Celes" or buddy["name"] == "Snow" or buddy["name"] == "Squall" or buddy["name"] == "Vanille": 
        #     print "Saved stats for: [" + buddy["name"] + " (id: " + str(buddy_id) + ") - level " + str(level) + "]"
        #     with open(test_file_path, 'w') as f:
        #         print >> f, json.dumps(buddy, indent=4, sort_keys=False)
        #     with open(json_file_path, 'w') as f:
        #         print >> f, json.dumps(buddy, indent=4, sort_keys=False)

        # not working correctly
        # if not (os.path.isfile(test_file_path)):
        #     test_file = open(test_file_path)
        #     print >> test_file, json.dumps(buddy, indent=4, sort_keys=True)
        #     test_file.close()

def get_soul_strike_info(data):
    #use with get battle init 
    ### TODO: UPDATE TO WORK WITH NEW CONTENT ###
    battle = data["battle"]
    for buddy in battle["buddy"]:
        a = buddy["soul_strike"]["ability_id"]
        if not os.access(os.getcwd() + "/data/soul_strikes/" + str(a) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/soul_strikes/" + str(a) + "/")

        test_file = open(os.getcwd() + "/data/soul_strikes/" + str(a) + "/" + str(a) + ".json",'w')
        print >> test_file, json.dumps(buddy.get("soul_strike","Error"), indent=4, sort_keys=True)
        test_file.close()

def uniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output

def get_enemy_stats_from_json(dungeon_id):
    temp = []
    enemy_file_path = os.getcwd() + "/enemy_data/" + dungeon_id  + ".json"

    with open(enemy_file_path, 'r') as f:
        temp = json.loads(f.read())

    return temp
 
def get_abilities_stats_from_json():
    temp = []
    enemy_file_path = os.getcwd() + "/data/abilities.json"

    with open(enemy_file_path, 'r') as f:
        temp = json.loads(f.read())

    return temp

def save_abilities(data, path):

    temp = []
    temp2 = []
    enemy_file_path = os.getcwd() + path + ".json"

    if os.path.isfile(enemy_file_path):
        temp = get_abilities_stats_from_json()

    # combine the two lists
    for ability in temp:
        temp2.append(ability)

    for ability in data:
        temp2.append(ability)

    # print temp2

    # remove duplicates
    temp3 = uniq(temp2)

    save_single_ability(temp3, str(path) + "/")

    enemy_output_file = open(os.getcwd() + path + ".json", 'w')
    enemy_output_file.seek(0)
    
    print >> enemy_output_file, json.dumps(temp3, indent=4, separators=(',', ': '), sort_keys=False)
    enemy_output_file.close()

def save_single_ability(data, path):

    for ability in data:
        temp_str = ability['options'].get("name","Error")
        a = temp_str.replace(" ", "_").lower()
        test_file = open(os.getcwd() + path + a + ".json",'w')
        print >> test_file, json.dumps(ability, indent=4, sort_keys=True)
        test_file.close()

def save_enemy_stats(data, dungeon_id):

    temp = []
    temp2 = []
    enemy_file_path = os.getcwd() + "/enemy_data/" + dungeon_id  + ".json"
    
    if os.path.isfile(enemy_file_path):
        temp = get_enemy_stats_from_json(dungeon_id)

    # combine the two lists
    for enemy in temp:
        temp2.append(enemy)

    for enemy in data:
        temp2.append(enemy)

    # print temp2

    enemy_output_file = open(os.getcwd() + "/enemy_data/" + dungeon_id + ".json", 'w')
    enemy_output_file.seek(0)
    
    print >> enemy_output_file, json.dumps(temp2, indent=4, separators=(',', ': '), sort_keys=False)
    enemy_output_file.close()

def save_equipment(data):
    temp = []
    for item in data["equipments"]:
        equipment_id = item.get("equipment_id","Error")
        level = item.get("level","0")
        name = item.get("name","Error")
        # name1 = name.replace("\uff0b","+")
        # name1 = name.replace("\xef","")
        utf8_str = name.encode('utf-8')
        name1 = name
        if '\xef' in utf8_str:
            # print str(equipment_id) + " " + utf8_str
            # name1 = utf8_str.replace("\xef","")
            name2 = re.split('\)', name)
            name1 = str(name2[0]) + ")"

        if ITEMS.get(equipment_id,"Not found") == "Not found":
            temp.append([equipment_id, name])
            # save_equipment_id(temp)
            # print name1
            save_equipment_id(equipment_id, name)
            # reload dict ITEMS dict?
            # doesnt work
            # ITEMS = __init__.load_dict("data/items.csv")

        if not os.access(os.getcwd() + "/data/equipment/" + str(equipment_id) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/equipment/" + str(equipment_id) + "/")
        
        file_path = os.getcwd() + "/data/equipment/" + str(equipment_id) + "/" + str(equipment_id) + "_level_" + str(level) + ".json"
        
        # if not os.path.isfile(file_path):
        if not os.access(file_path, os.F_OK):
            print "Saved stats for: [" + str(name1) + " (id: " + str(equipment_id) + ") - level " + str(level) + "]"
            test_file = open(file_path,'w')
            print >> test_file, json.dumps(item, indent=4, sort_keys=True)
            test_file.close()

def save_equipment_list(data, user_id):
    equipment_list_file = open("current_equipment/current_equipment_" + str(user_id) + time.strftime("%m%d%Y-%H%M%S")+".json", 'w')
    print >> equipment_list_file, "{\n\t\"equipments\": " + json.dumps(data["equipments"], indent=4, sort_keys=False)
    print >> equipment_list_file, "}"
    equipment_list_file.close()

def get_display_name(enemy):
    for child in enemy["children"]:
        for param in child["params"]:
            return param.get("disp_name", "Unknown Enemy")

def get_enemy_hp(enemy):
    for child in enemy["children"]:
        # return child.get("max_hp", "Unknown HP")
        for param in child["params"]:
            return param.get("max_hp", "Unknown HP")

def get_drops(enemy):
    for child in enemy["children"]:
        for drop in child["drop_item_list"]:
            yield drop

def get_buddy_name(buddy):
    # for param in buddy["params"]:
    return child.get("max_hp", "Unknown HP")
        # return param.get("disp_name", "Unknown name")

def get_user_id(data):
    # for param in data["party"]:
    return data["party"].get("user_id", "Unknown user_id")
        # return param.get("disp_name", "Unknown name")

def handle_get_battle_init_data(data):
    enemy_list = []
    ability_list = []
    soul_strike_list = []
    enemy_ability_list = []
    character_list = []

    pp = pprint.PrettyPrinter(indent=4)

    # log data
    debug_path = os.getcwd() + "/data/raw/handle_get_battle_init_data/handle_get_battle_init_data_" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
    test_file = open(debug_path, 'w')
    print >> test_file, json.dumps(data, indent=4, sort_keys=False)
    test_file.close()

    battle_data = data["battle"]
    battle_id = battle_data["battle_id"]
    battle_name = BATTLES.get(battle_id, "battle #" + battle_id)
    print ""
    print "Entering {0}".format(battle_name)
    all_rounds_data = battle_data['rounds']
    tbl = [["rnd", "enemy", "hp", "drop"]]
    for round_data in all_rounds_data:
        round = round_data.get("round", "???")
        for round_drop in round_data["drop_item_list"]:
            item_type = int(round_drop.get("type", 0))
            if item_type == 21:
                itemname = "potion"
            elif item_type == 22:
                itemname = "hi-potion"
            elif item_type == 23:
                itemname = "x-potion"
            elif item_type == 31:
                itemname = "ether"
            elif item_type == 32:
                itemname = "turbo ether"
            else:
                itemname = "unknown"
            tbl.append([round, "<round drop>","", itemname])
        for enemy in round_data["enemy"]:
            had_drop = False
            enemyname = get_display_name(enemy)
            enemyhp = get_enemy_hp(enemy)
            for drop in get_drops(enemy):
                item_type = drop.get("type", 0)
                if item_type == 11:
                    itemname = "{0} gil".format(drop.get("amount", 0))
                elif item_type == 41 or item_type == 51:
                    type_name = "orb id#" if item_type == 51 else "equipment id#"
                    item = ITEMS.get(drop["item_id"], type_name + drop["item_id"])
                    itemname = "{0}* {1}".format(drop.get("rarity", 1), item)
                elif item_type == 61:
                    itemname = "event item"
                else:
                    itemname = "unknown"
                had_drop = True
                tbl.append([round, enemyname, enemyhp, itemname])
            if not had_drop:
                tbl.append([round, enemyname, enemyhp, "nothing"])
            # for child in enemy["children"]

            enemy_list.append(enemy)
            # print enemy_list
            # pp.pprint(enemy_list)

    # print "enemy_list: " + str(len(enemy_list))
    print tabulate(tbl, headers="firstrow")
    print ""
    # print tabulate(tbl)

    save_enemy_stats(enemy_list, battle_id)

# fire/blizzard/thunder/dark/-ara/-aga/-aja
# arg1 = power multiplier
# arg2 = element 
# arg3 = ?
# arg4 = ?
# arg5 = ?

# elements
# 100 = fire
# 101 = ice
# 102 = thunder
# 103 = earth
# 104 = wind
# 105 = water
# 106 = holy(cure/a/aga/aja)
# 107 = dark
# 108 = poison


# "status_ailments_factor" = % chance to inflict status ailment
# "status_ailments_id" = ID for status ailment
# 200 = poison
# 201 = silence
# 202 = paralyze
# 203 = confuse
# 204 = haste
# 205 = slow
# 206 = stop
# 207 = protect
# 208 = shell
# 209 = reflect
# 210 = blind
# 211 = sleep
# 212 = stone/pretrify
# 213 = ? Doom ?
# 214 = instant KO (death)/gravity/cripple
# 215 = ? Berserk ?
# 216 = regen

# ### For "attribute_id": "1XX" ####

# "factor": "1" = this means that said enemy is weak to the element with that corresponding attribute_id
# "factor": "6" = this means that said enemy resists the corresponding element
# "factor": "11" = this means that said enemy nulls (takes zero damage from) the corresponding element
# "factor": "21" = this means that said enemy absorbs the corresponding element


# ### For "attribute_id": "2XX" ####
# "factor": "1" = with a factor of one and the attribute_id preset to "2XX", it means said enemy is immune to that debuff


    # ability data
    buddy_data = battle_data["buddy"]
    for buddy in buddy_data:
        for ability in buddy["abilities"]:
            ability_list.append(ability)
       

    # only need to save abilities when new ones come out or create the ones I don't have

    enemy_ability_data = battle_data["enemy_abilities"]
    for enemy_ability in enemy_ability_data:
        enemy_ability_list.append(enemy_ability)

    # print "\nsoul_stike_list:\n" 
    # # print soul_strike_list
    # for option in soul_strike_list["options"]:
    #     print option
    # print "\ncharacter_list:\n"
    # print character_list
    # print enemy_ability_list

    save_abilities(ability_list, "/data/abilities")
    # save_abilities(soul_strike_list, "/data/soul_strikes")
    save_abilities(enemy_ability_list, "/data/enemy_abilities")
    # save_enemy_abilities(enemy_ability_list)

    # TODO: Update to use new content/structure, DONE just at work computer
    # get_soul_strike_info(data)

    #TODO
    # w = []

    # if temp_party_list:
    #     for buddy in temp_party_list["buddies"]:
    #         w.append({'buddy_id': str(buddy.get(buddy_id)), 'record_materia_1_id': str(buddy.get(record_materia_1_id))})

    # buddy_data = battle_data["buddy"]
    #     for buddy in buddy_data:
    #         if buddy["buddy_id"]

def handle_party_list(data):

    # log data
    debug_path = os.getcwd() + "/data/raw/handle_party_list/handle_party_list_" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
    test_file = open(debug_path, 'w')
    print >> test_file, json.dumps(data, indent=4, sort_keys=False)
    test_file.close()

    wanted = "name series_id acc atk def eva matk mdef mnd series_acc series_atk series_def series_eva series_matk series_mdef series_mnd"
    topn = OrderedDict()
    topn["atk"] = 5
    topn["matk"] = 5
    topn["mnd"] = 3
    topn["def"] = 5
    topn["mdef"] = 3
    find_series = [200001, 101001, 102001, 103001, 104001, 105001, 106001, 107001, 108001, 109001, 110001, 112001, 113001]
    equips = defaultdict(list)
    for item in data["equipments"]:
        kind = item.get("equipment_type", 1)
        heapq.heappush(equips[kind], Equipment(slicedict(item, wanted)))

    for series in find_series:
        if series == 200001:
            print "Best equipment for FF Core"
        else:
            print "Best equipment for FF{0}:".format((series - 100001) / 1000)

        # Need to use lists for column ordering
        tbl = ["stat n weapon stat n armor stat n accessory".split()]
        tbldata = [[],[],[],[]]
        for itemtype in range(1, 4): ## 1, 2, 3
            for stat, count in topn.iteritems():
                for equip in best_equipment(series, equips[itemtype], stat, count):
                    name = equip["name"].replace(u"\uff0b", "+")
                    tbldata[itemtype].append([stat, equip[stat], name])

        # Transpose data
        for idx in range(0, len(tbldata[1])):
            tbl.append(tbldata[1][idx] + tbldata[2][idx] + tbldata[3][idx])
        print tabulate(tbl, headers="firstrow")
        print ""

    # print equipment to json file
    save_equipment_list(data, get_user_id(data))
    save_equipment(data)

    get_buddy_info(data)
    temp_party_list = data

def handle_dungeon_list(data):

    # log data
    debug_path = os.getcwd() + "/data/raw/handle_dungeon_list/handle_dungeon_list_" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
    test_file = open(debug_path, 'w')
    print >> test_file, json.dumps(data, indent=4, sort_keys=False)
    test_file.close()

    tbl = []
    world_data = data["world"]
    world_id = world_data["id"]
    world_name = world_data["name"]
    print "Dungeon List for {0} (id={1})".format(world_name, world_id)
    dungeons = data["dungeons"]
    for dungeon in dungeons:
        name = dungeon["name"]
        id = dungeon["id"]
        difficulty = dungeon["challenge_level"]
        type = "ELITE" if dungeon["type"] == 2 else "NORMAL"
        tbl.append([name, id, difficulty, type])
    tbl = sorted(tbl, key=lambda row : int(row[1]))
    tbl.insert(0, ["Name", "ID", "Difficulty", "Type"])
    print tabulate(tbl, headers="firstrow")

def handle_battle_list(data):

    # log data
    debug_path = os.getcwd() + "/data/raw/handle_battle_list/handle_battle_list_" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
    test_file = open(debug_path, 'w')
    print >> test_file, json.dumps(data, indent=4, sort_keys=False)
    test_file.close()
    
    temp = []
    tbl = [["Name", "Id", "Rounds"]]
    dungeon_data = data["dungeon_session"]
    dungeon_id = dungeon_data["dungeon_id"]
    dungeon_name = dungeon_data["name"]
    dungeon_type = int(dungeon_data["type"])
    world_id = dungeon_data["world_id"]
    series_id = dungeon_data["series_id"]
    difficulty = dungeon_data["challenge_level"]
    Type = dungeon_data["type"]
    print "Entering dungeon {0} ({1})".format(dungeon_name, "Elite" if dungeon_type==2 else "Normal")
    battles = data["battles"]

    for battle in battles:
        d_id = battle["dungeon_id"]
        has_boss = battle["has_boss"]
        ID = battle["id"]
        name = battle["name"]
        rounds = battle["round_num"]
        stamina = battle["stamina"]
        tbl.append([battle["name"], battle["id"], battle["round_num"]])
        temp.append([d_id, series_id, ID, name, difficulty, Type, rounds, stamina, has_boss])
    save_battles(temp)
    print tabulate(tbl, headers="firstrow")

# {
#       "dungeon_id": 620072,
#       "has_boss": 0,
#       "id": 720226,
#       "is_unlocked": false,
#       "name": "Gil Greenwood - Heroic, Part 1",
#       "order_no": 1,
#       "rank": 0,
#       "round_num": 3,
#       "stamina": 15
#     }

def handle_survival_event(data):
    # XXX: This maybe works for all survival events...
    enemy = data.get("enemy", dict(name="???", memory_factor="0"))
    name = enemy.get("name", "???")
    factor = float(enemy.get("memory_factor", "0"))
    print "Your next opponent is {0} (x{1:.1f})".format(name, factor)

def log_data(data, var):
    path_dir = os.getcwd() + "/data/raw/" + str(var) + "/"
    if not os.access(path_dir, os.F_OK):
        os.mkdir(path_dir)

    # print path_dir
    if os.path.isdir(path_dir):
        # print "var: " + var
        path = path_dir + str(var) + "_" + time.strftime("%m%d%Y-%H%M%S") + ".json" 
        test_file = open(path, 'w')
        print >> test_file, json.dumps(data, indent=4, sort_keys=False)
        test_file.close()

def handle_home(data):
    var = "dff"
    log_data(data,var)

def handle_splash(data):
    var = "splash"
    log_data(data,var)

def handle_timestamp(data):
    var = "timestamp"
    log_data(data,var)

def handle_battle_timestamp(data):
    var = "battle_timestamp"
    log_data(data,var)

def handle_api_create_session(data):
    var = "api_create_session"
    log_data(data,var)

def handle_notification_check(data):
    var = "notification_check"
    log_data(data,var)
    
def handle_get_google_achievements(data):
    var = "get_google_play_achievements"
    log_data(data,var)
    
def handle_update_user_session(data):
    var = "update_user_session"
    log_data(data,var)
    
def handle_menu_friend(data):
    var = "menu_friend"
    log_data(data,var)
    
def handle_gift_box_get_data(data):
    var = "gift_box_get_data"
    log_data(data,var)
    
def handle_gift_box_receive_all(data):
    var = "gift_box_receive_all"
    log_data(data,var)
    
def handle_gift_box(data):
    var = "gift_box"
    log_data(data,var)
    
def handle_gacha_show(data):
    var = "gacha_show"
    log_data(data,var)
    
def handle_notification_popup(data):
    var = "notification_popup"
    log_data(data,var)

def handle_gacha_probability_series(data):
    var = "gacha_probability_series"
    log_data(data,var)
    
def handle_gacha_probability(data):
    var = "gacha_probability"
    log_data(data,var)

def handle_get_root_data(data):
    var = "get_root_data"
    log_data(data,var)

def handle_gacha(data):
    var = "gacha"
    log_data(data,var)

def handle_buddy_save_equipment(data):
    var = "buddy_save_equipment"
    log_data(data,var)

def handle_equipment_enhance(data):
    var = "equipment_enhance"
    log_data(data,var)
    base_dir_path = "/data/equipment/"

    save_single_equipment_by_id(data["new_src_user_equipment"], base_dir_path)
    save_single_equipment_by_id(data["old_src_user_equipment"], base_dir_path)

def handle_buddy_save_ability(data):
    var = "buddy_save_ability"
    log_data(data,var)

def handle_grow_egg_get_buddy_level_to_exp_map(data):
    var = "grow_egg_get_buddy_level_to_exp_map"
    log_data(data,var)

def handle_grow_egg_use(data):
    var = "grow_egg_use"
    log_data(data,var)

    buddy = data["buddy"]
    level = buddy.get("level","Unknown")
    job_name = buddy.get("job_name", "Unknown")

    # Tyro check
    if job_name == "Keeper":
        buddy["name"] = "Tyro"

    temp_str = buddy.get("name", "Unknown")

    if job_name == "Dark Knight" and buddy["name"] == "Cecil":
        #buddy["name"] = "CecilDK"
        temp_str = "CecilDK"

    if job_name == "Paladin" and buddy["name"] == "Cecil":
        #buddy["name"] = "CecilP"
        temp_str = "CecilP"

    a = temp_str.replace(" ", "_").lower()

    if not os.access(os.getcwd() + "/data/buddy/" + a + "/", os.F_OK):
        os.mkdir(os.getcwd() + "/data/buddy/" + a + "/")

    if not os.access(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/", os.F_OK):
        os.mkdir(os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/")

    test_file_path = os.getcwd() + "/data/buddy/" + a + "/" + str(level) + "/" + a + "_level_" + str(level) + "_stats.json"  
    with open(test_file_path, 'w') as f:
        print >> f, json.dumps(buddy, indent=4, sort_keys=False)

def handle_gacha_execute(data):
    var = "gacha_execute"
    log_data(data,var)

def handle_js_log(data):
    var = "js_log"
    log_data(data,var)

def handle_payment_create(data):
    var = "payment_create"
    log_data(data,var)

def handle_payment_update(data):
    var = "payment_update"
    log_data(data,var)

def start(context, argv):
    global args
    
    from recordpeeker.command_line import parse_args
    args = parse_args(argv)
    ips = set([ii[4][0] for ii in socket.getaddrinfo(socket.gethostname(), None) if ii[4][0] != "127.0.0.1"])
    print "Configure your phone's proxy to point to this computer, then visit mitm.it"
    print "on your phone to install the interception certificate.\n"
    print "Record Peeker is listening on port {0}, on these addresses:".format(args.port)
    print "\n".join(["  * {0}".format(ip) for ip in ips])
    print ""
    print "Try entering the Party screen, or starting a battle."

    global dp
    dp = Dispatcher('ffrk.denagames.com')
    [dp.register(path, function) for path, function in handlers]
    [dp.ignore(path, regex) for path, regex in ignored_requests]

handlers = [
    ('get_battle_init_data' , handle_get_battle_init_data),
    ('/dff/party/list', handle_party_list),
    ('/dff/world/dungeons', handle_dungeon_list),
    ('/dff/world/battles', handle_battle_list),
    ('/dff/event/coliseum/6/get_data', handle_survival_event),
    # ('/dff/', handle_home),
    # ('/dff/splash', handle_splash),
    # ('/dff/?timestamp', handle_timestamp),
    # ('/dff/battle/?timestamp', handle_battle_timestamp),
    # ('/dff/_api_create_session', handle_api_create_session),
    ('/dff/notification/check', handle_notification_check),
    ('/dff/google_play_achievement/get_achievements', handle_get_google_achievements),
    # ('/dff/update_user_session', handle_update_user_session),
    ('/dff/menu/friend', handle_menu_friend),
    ('/dff/gift_box/get_data', handle_gift_box_get_data),
    ('/dff/gift_box/receive_all',handle_gift_box_receive_all),
    ('/dff/gift_box',handle_gift_box),
    ('/dff/gacha/show',handle_gacha_show),
    ('/dff/notification/mark_popuped',handle_notification_popup),
    ('/dff/gacha/probability?series_id',handle_gacha_probability_series),
    ('/dff/gacha/probability',handle_gacha_probability),
    ('/dff/get_root_data',handle_get_root_data),
    ('/dff/gacha',handle_gacha),
    ('/dff/buddy/save_equipment',handle_buddy_save_equipment),
    ('/dff/equipment/enhance',handle_equipment_enhance),
    ('/dff/buddy/save_ability',handle_buddy_save_ability),
    ('/dff/grow_egg/get_buddy_level_to_exp_map',handle_grow_egg_get_buddy_level_to_exp_map),
    ('/dff/grow_egg/use', handle_grow_egg_use),
    ('/dff/gacha/execute',handle_gacha_execute),
    ('/dff/js/log',handle_js_log),
    ('/dff/payment/create',handle_payment_create),
    ('/dff/payment/update',handle_payment_update)
]
# #added ones
# /dff/party_memory/list
# /dff/party_memory/save
# /dff/event/challenge/503/win_battle
# /dff/menu/friend
# /dff/get_root_data
# /dff/event/challenge/503/enter
# /dff/event/challenge/503/get_data
# /dff/world/dungeons?world_id=107006
# /dff/event/challenge/503/get_data
# /dff/relation/detailed_fellow_listing
# /dff/event/challenge/503/enter_dungeon
# /dff/world/battles
# /dff/event/challenge/503/begin_battle_session
# /dff/event/challenge/503/begin_battle
# /dff/battle/?timestamp=1438746064&battle_id=707186
# /dff/event/challenge/503/get_battle_init_data





# /dff/buddy/save_equipment
# /dff/equipment/enhance
# /dff/_api_create_session
# /dff/notification/check
# /dff/google_play_achievement/get_achievements
# /dff/update_user_session
# /dff/menu/friend
# /dff/gift_box/get_data
# /dff/gift_box/receive_all
# /dff/gacha/show
# /dff/notification/mark_popuped
# /dff/gacha/probability?series_id=29
# /dff/get_root_data
# /dff/world/dungeons?world_id=107001
# /dff/party/list

# /dff/splash
# https://ffrk.static.denagames.com/dff/static/ww/compile/en/js/direct/sakura.js?_=1423216230
# https://ffrk.static.denagames.com/dff/static/ww/compile/en/js/direct/anchors.js?_=1423216230
# /dff/
# /dff/world/enter_dungeon
# /dff/world/battles
# /dff/battle/begin_session
# /dff/battle/begin_battle
# /dff/battle/?timestamp=1438650977&battle_id=307004
# /dff/battle/get_battle_init_data
# /dff/battle/win
# /dff/world/epilogue?dungeon_id=207002 

ignored_requests = [
    ('/dff/', True),
    ('/dff/splash', False),
    ('/dff/?timestamp', False),
    ('/dff/battle/?timestamp', False),
]

def response(context, flow):
    global args
    global dp
    dp.handle(flow, args)
