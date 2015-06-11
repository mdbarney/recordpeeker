import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
from collections import OrderedDict, defaultdict

from libmproxy.protocol.http import decoded
from tabulate import tabulate

from recordpeeker import Equipment, ITEMS, BATTLES, DUNGEONS, slicedict, best_equipment
from recordpeeker.dispatcher import Dispatcher

current_dungeon_id = 0

# TODO
# def save_dungeons(data):

# TODO
# def save_battles(data):

def get_enemy_stats_from_json(dungeon_id):
    temp = []
    enemy_file_path = os.getcwd() + "/enemy_data/" + dungeon_id  + ".json"

    with open(enemy_file_path, 'r') as f:
        temp = json.loads(f.read())

    return temp
        
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
    
    print >> enemy_output_file, json.dumps(temp2, indent=4, separators=(',', ': '), sort_keys=True)
    enemy_output_file.close()

def save_equipment_list(data):
    equipment_list_file = open("current_equipment.json", 'w')
    print >> equipment_list_file, "{\n\t\"equipments\": " + json.dumps(data["equipments"], indent=4, sort_keys=True)
    print >> equipment_list_file, "}"
    equipment_list_file.close()

def get_display_name(enemy):
    for child in enemy["children"]:
        for param in child["params"]:
            return param.get("disp_name", "Unknown Enemy")

def get_drops(enemy):
    for child in enemy["children"]:
        for drop in child["drop_item_list"]:
            yield drop


def handle_get_battle_init_data(data):
    # enemy_stats_file = open("enemy.json", 'w')
    enemy_list = []

    # # prints out current data list
    # test_file = open("data.json", 'w')
    # print >> test_file, json.dumps(data, indent=4, sort_keys=True)

    battle_data = data["battle"]
    battle_id = battle_data["battle_id"]
    battle_name = BATTLES.get(battle_id, "battle #" + battle_id)
    print "Entering {0}".format(battle_name)
    all_rounds_data = battle_data['rounds']
    tbl = [["rnd", "enemy", "drop"]]
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
            tbl.append([round, "<round drop>", itemname])
        for enemy in round_data["enemy"]:
            had_drop = False
            enemyname = get_display_name(enemy)
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
                tbl.append([round, enemyname, itemname])
            if not had_drop:
                tbl.append([round, enemyname, "nothing"])

            enemy_list.append(enemy)

        # print >> enemy_stats_file, json.dumps(round_data["enemy"], indent=4, sort_keys=True)
        # print >> enemy_stats_file, json.dumps(enemy_list, indent=4, sort_keys=True)
    save_enemy_stats(enemy_list, battle_id)

    print tabulate(tbl, headers="firstrow")
    print ""
    # enemy_stats_file.close()

def handle_party_list(data):
    wanted = "name series_id acc atk def eva matk mdef mnd series_acc series_atk series_def series_eva series_matk series_mdef series_mnd"
    topn = OrderedDict()
    topn["atk"] = 5
    topn["matk"] = 5
    topn["mnd"] = 3
    topn["def"] = 5
    find_series = [101001, 102001, 103001, 104001, 105001, 106001, 107001, 108001, 110001, 113001]
    equips = defaultdict(list)
    for item in data["equipments"]:
        kind = item.get("equipment_type", 1)
        heapq.heappush(equips[kind], Equipment(slicedict(item, wanted)))

    for series in find_series:
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
    save_equipment_list(data)

def handle_dungeon_list(data):
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
    tbl = [["Name", "Id", "Rounds"]]
    dungeon_data = data["dungeon_session"]
    dungeon_id = dungeon_data["dungeon_id"]
    dungeon_name = dungeon_data["name"]
    dungeon_type = int(dungeon_data["type"])
    world_id = dungeon_data["world_id"]
    print "Entering dungeon {0} ({1})".format(dungeon_name, "Elite" if dungeon_type==2 else "Normal")
    battles = data["battles"]
    for battle in battles:
        tbl.append([battle["name"], battle["id"], battle["round_num"]])
    print tabulate(tbl, headers="firstrow")

def handle_survival_event(data):
    # XXX: This maybe works for all survival events...
    enemy = data.get("enemy", dict(name="???", memory_factor="0"))
    name = enemy.get("name", "???")
    factor = float(enemy.get("memory_factor", "0"))
    print "Your next opponent is {0} (x{1:.1f})".format(name, factor)

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
    ('/dff/event/coliseum/6/get_data', handle_survival_event)
]

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
