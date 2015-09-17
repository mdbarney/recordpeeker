import json
import shlex
import os
import socket
import heapq
import fileinput
import os.path
import pprint
import csv
import re
from collections import OrderedDict, defaultdict

def load_dict(path):
    with open(path, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = dict((rows[0],rows[1]) for rows in reader)
    return mydict

def get_buddy_info(data):
    # use with party_list
    ### TODO ### make this use id rather than names
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
        with open(test_file_path, 'w') as f:
            print >> f, json.dumps(buddy, indent=4, sort_keys=False)
        

        if not os.access(os.getcwd() + json_path + str(buddy_id) + "/", os.F_OK):
            os.mkdir(os.getcwd() + json_path + str(buddy_id) + "/")

        json_file_path = os.getcwd() + json_path + str(buddy_id) + "/" + a + "_level_" + str(level) + "_stats.json"  
        with open(json_file_path, 'w') as f:
            print >> f, json.dumps(buddy, indent=4, sort_keys=False)

        # not working correctly
        # if not (os.path.isfile(test_file_path)):
        #     test_file = open(test_file_path)
        #     print >> test_file, json.dumps(buddy, indent=4, sort_keys=True)
        #     test_file.close()

def get_soul_strike_info(data):
    #use with get battle init 
    battle = data["battle"]
    for buddy in battle["buddy"]:
        for soul_strike in buddy["soul_strikes"]:
            a = soul_strike["ability_id"]
            if not os.access(os.getcwd() + "/data/soul_strikes/" + str(a) + "/", os.F_OK):
                os.mkdir(os.getcwd() + "/data/soul_strikes/" + str(a) + "/")

                test_file = open(os.getcwd() + "/data/soul_strikes/" + str(a) + "/" + str(a) + ".json",'w')
                print >> test_file, json.dumps(soul_strike, indent=4, sort_keys=False)
                test_file.close()

def get_record_materia_info(data):
    #use with get battle init 
    battle = data["battle"]
    for buddy in battle["buddy"]:
        for materia in buddy["materias"]:
            a = materia["arg1"]
            print a
            if not os.access(os.getcwd() + "/data/record_materia/" + str(a) + "/", os.F_OK):
                os.mkdir(os.getcwd() + "/data/record_materia/" + str(a) + "/")

                test_file = open(os.getcwd() + "/data/record_materia/" + str(a) + "/" + str(a) + ".json",'w')
                print >> test_file, json.dumps(materia, indent=4, sort_keys=False)
                test_file.close()

def get_record_materia_from_party_list(data):
    #use with handle party list
    for materia in data["record_materias"]:
        a = materia["record_materia_id"]
        print a
        if not os.access(os.getcwd() + "/data/record_materia/" + str(a) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/record_materia/" + str(a) + "/")

            test_file = open(os.getcwd() + "/data/record_materia/" + str(a) + "/" + str(a) + ".json",'w')
            print >> test_file, json.dumps(materia, indent=4, sort_keys=False)
            test_file.close()


def build_equipment_stat_file():
	name = ""
	path = str(os.getcwd()) + "/data/equipment/"
	csv_path = str(os.getcwd()) + "/data/csv/equipment/"
	for dir_entry in os.listdir(path):
		temp = []
		dir_entry_path = os.path.join(path, dir_entry)

		if os.path.isdir(dir_entry_path):
		#print dir_entry        
			for f in os.listdir(dir_entry_path):
				#print str(file_path) + "/" + str(f)
				b = os.path.join(dir_entry_path, f)
				print b
				if os.path.isfile(b):
					with open(b, 'rb') as my_file:
						e = json.loads(my_file.read())
						if e.get("spd","error") == "error":
							e["spd"] = 0
						if e.get("series_spd","error") == "error":
							e["series_spd"] = 0
						temp.append(e)
						name = e["name"]
						utf8_str = name.encode('utf-8')
						name1 = name
						if '\xef' in utf8_str:
							# print str(equipment_id) + " " + utf8_str
							# name1 = utf8_str.replace("\xef","")
							name2 = re.split('\)', name)
							name1 = str(name2[0]) + ")"

			# print temp
			name_flag = 0
			with open(csv_path + dir_entry + '_' + name1 + '.csv', 'w') as csvfile:
				fieldnames = [name1,'level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
				# fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
				writer.writeheader()
				for t in temp:
					# writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
					writer.writerow({name1:"",'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
                    
def build_buddy_stat_file():
    path = str(os.getcwd()) + "/data/buddy/"
    csv_path = str(os.getcwd()) + "/data/csv/buddy/"
    for dir_entry in os.listdir(path):
        temp = []
        dir_entry_path = os.path.join(path, dir_entry)

        # p = "/home/rockwell/Desktop/csv/" + dir_entry + '.csv'
        # if os.path.isfile(p):
        #     with open(p, 'rb') as c:
        #         csv_data = csv.reader(csvfile, delimiter=' ', quotechar='|')

        # if os.access(os.getcwd() + "/data/buddy/" + a + "/", os.F_OK):
        #if os.path.isfile(dir_entry_path):
        #    with open(dir_entry_path, 'r') as my_file:
                # data[dir_entry] = my_file.read()
        #        data[dir_entry] = json.loads(my_file.read())

        if os.path.isdir(dir_entry_path):
            #print dir_entry
            for level_dir in os.listdir(dir_entry_path):
                file_path = os.path.join(dir_entry_path, level_dir)
                #print os.listdir(file_path)
                if os.path.isdir(file_path):
                    for f in os.listdir(file_path):
                        #print str(file_path) + "/" + str(f)
                        b = os.path.join(file_path, f)
                        print b
                        if os.path.isfile(b):
                            with open(b, 'rb') as my_file:
                                temp.append(json.loads(my_file.read()))
            
                # print temp
                with open(csv_path + dir_entry + '.csv', 'w') as csvfile:
                    fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_level', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
                    # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

                    writer.writeheader()
                    for t in temp:
                        # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
                        writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"],'series_level': t["series_level"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
                        

    #print temp
    #for t in temp:
     #   print t["name"]

def getKey(item):
    return item['level']

def sort_buddy_csv_by_attribute(file_path, attribute):
    for dir_entry in os.listdir(file_path):
        num_rows = 0
        temp = []
        dir_entry_path = os.path.join(file_path, dir_entry)
        print dir_entry_path
        if os.path.isfile(dir_entry_path):
            temp = []
            fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_level', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            with open(dir_entry_path, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    temp.append(row)
                    num_rows = num_rows + 1

            # convert parameters to ints for sorting
            for p in temp:
                for q in fieldnames:
                    p[q] = int(p[q])
            # print temp

            # temp1 = sorted(temp, key=itemgetter(attribute))
            temp1 = sorted(temp, key=getKey)

            with open(dir_entry_path, 'w') as csvfile:
                # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

                writer.writeheader()
                for t in temp1:
                    # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
                    writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"],'series_level': t["series_level"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
            
            # if num_rows > 2:
            #     with open(file_path + "/../multi_buddy/" + dir_entry, 'w') as csvfile:
            #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            #         writer.writeheader()
            #         for t in temp1:
            #             # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
            #             writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"],'series_level': t["series_level"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
            
def sort_equip_csv_by_attribute(file_path, attribute):
    for dir_entry in os.listdir(file_path):
        temp = []
        name = ""
        num_rows = 0
        dir_entry_path = os.path.join(file_path, dir_entry)
        print dir_entry_path
        if os.path.isfile(dir_entry_path):
            temp = []
            qq = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            with open(dir_entry_path, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                h_flag = 0
                for row in reader:
                    if h_flag == 0:
                        for f in row.keys():
                            if f not in qq:
                                name = f
                                h_flag = 1
                    # print row
                    temp.append(row)
                    num_rows = num_rows + 1

            # convert parameters to ints for sorting
            for p in temp:
                for q in qq:
                    p[q] = int(p[q])
            # print temp

            # temp1 = sorted(temp, key=itemgetter(attribute))
            temp1 = sorted(temp, key=getKey)

            with open(dir_entry_path, 'w') as csvfile:
                # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
                fieldnames = [name, 'level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

                writer.writeheader()
                # writer.writerow(t_header)
                for t in temp1:
                    # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
                    writer.writerow({name:'','level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
                
            # if num_rows > 2:
            #     with open(file_path + "/../multi_equip/" + dir_entry, 'w') as csvfile:

            #         # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
            #         fieldnames = [name, 'level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            #         writer.writeheader()
            #         # writer.writerow(t_header)
            #         for t in temp1:
            #             # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
            #             writer.writerow({name:'','level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})

def build_equipment_compare_file():
    path = str(os.getcwd()) + "/data/equipment/"
    csv_path = "/home/rockwell/Desktop/csv/equipment/"

    one_star = []
    two_star = []
    three_star = []
    four_star = []
    five_star = []

    for dir_entry in os.listdir(path):
        temp = []
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isdir(dir_entry_path):
            # print dir_entry_path
            for level_dir in os.listdir(dir_entry_path):
                file_path = os.path.join(dir_entry_path, level_dir)
                print file_path
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as my_file:
                        a = json.loads(my_file.read())
                        if a.get("spd","0") == "0":
                            a["spd"] = 0
                        if a.get("series_spd","0") == "0":
                            a["series_spd"] = 0

                        
                        temp.append(a)

                    # for f in os.listdir(file_path):
                    #     #print str(file_path) + "/" + str(f)
                    #     b = os.path.join(file_path, f)
                    #     print b
                    #     if os.path.isfile(b):
                    #         with open(b, 'rb') as my_file:
                    #             temp.append(json.loads(my_file.read()))
            
                # print temp
                temp1 = sorted(temp, key=itemgetter('level')) 

                name = a.get("name","Error")
                utf8_str = name.encode('utf-8')
                name1 = name
                if '\xef' in utf8_str:
                    name2 = re.split('\)', name)
                    name1 = str(name2[0]) + ")"

                name3 = name1.replace(" ", "_").replace("\'","").lower()


            # if



            with open(csv_path + dir_entry + '_' + name3 +'.csv', 'w') as csvfile:
                fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
                # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

                writer.writeheader()
                for t in temp1:
                    # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
                    writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
                    # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t.get("spd",0),'series_level': t["series_level"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t.get("series_spd",0)})
                        

            # # try this
            #  with open(dir_entry_path, 'w') as csvfile:
            #     # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
            #     fieldnames = [name, 'level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            #     writer.writeheader()
            #     # writer.writerow(t_header)
            #     for t in temp1:
            #         # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
            #         writer.writerow({name:'','level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})
                
            # if num_rows > 2:
            #     with open(file_path + "/../multi_equip/" + dir_entry, 'w') as csvfile:
            #         # fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd']
            #         fieldnames = [name, 'level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            #         writer.writeheader()
            #         # writer.writerow(t_header)
            #         for t in temp1:
            #             # writer.writerow({'level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"]})
            #             writer.writerow({name:'','level': t["level"], 'hp': t["hp"], 'atk': t["atk"], 'matk': t["matk"], 'acc': t["acc"], 'def': t["def"], 'mdef': t["mdef"], 'eva': t["eva"], 'mnd': t["mnd"], 'spd': t["spd"], 'series_hp': t["series_hp"], 'series_atk': t["series_atk"], 'series_matk': t["series_matk"], 'series_acc': t["series_acc"], 'series_def': t["series_def"], 'series_mdef': t["series_mdef"], 'series_eva': t["series_eva"], 'series_mnd': t["series_mnd"], 'series_spd': t["series_spd"]})


def get_drop_list(enemy):
    drop_list = []
    for child in enemy["children"]:
        for drops in child["drop_item_list"]:
            drop_list.append(drops)

    return drop_list

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
    #   temp.append(a)

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

def build_char_data(path):
	# can be either of these
	# path = os.getcwd() + "/data/raw/handle_party_list/"
    # path = os.getcwd() + "/debug/handle_party_list/"
    buddy_path = os.getcwd() + path
    for dir_entry in os.listdir(buddy_path):
        dir_entry_path = os.path.join(buddy_path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                # data[dir_entry] = my_file.read()
                # data[dir_entry] = json.loads(my_file.read())
                d = json.loads(my_file.read())
            get_buddy_info(d)


def get_item_max_number_of_levels(rarity):

    result = 0
    if rarity == 1:
        result = 10
    elif rarity == 2:
        result = 15
    elif rarity == 3:
        result = 20
    elif rarity == 4:
        result = 25
    elif rarity == 5:
        result = 30

    return result


def build_max_level_list(max_level):
    a = []
    i = 1
    while i <= max_level:
        a.append(i)
        i += 1

    return a

def get_items_logged():
    path = str(os.getcwd()) + "/data/equipment/"
    csv_path = str(os.getcwd()) + "/logged_items.csv"
    log = []
    for dir_entry in os.listdir(path):
        temp = []
        dir_entry_path = os.path.join(path, dir_entry)

        if os.path.isdir(dir_entry_path):
            #print dir_entry
            for level_dir in os.listdir(dir_entry_path):
                file_path = os.path.join(dir_entry_path, level_dir)
                #print os.listdir(file_path)
                with open(file_path, 'r') as f:
                    d = json.loads(f.read())
                # t = dict()
                name = d.get("name","error")
                utf8_str = name.encode('utf-8')
                name1 = name
                if '\xef' in utf8_str:
	                name2 = re.split('\)', name)
	                name1 = str(name2[0]) + ")"

                level = re.split('_', level_dir)
                level1 = str(level[2])
                level2 = re.split("\.",level1)
                level3 = level2[0]
                temp.append(int(level3))
                
            temp1 = sorted(temp)
            q = ""
            for tt in temp1:
            	q = str(q) +","+ str(tt)
            t = {'name': name1, 'levels': q}
            # temp1.insert(0,name)
            log.append(t)

    with open(csv_path, 'w') as f:
    	for t in log:
    		print t["name"] + str(t["levels"])
    		print >> f, str(t["name"]) + str(t["levels"])

def get_items_not_logged():
    path = str(os.getcwd()) + "/data/equipment/"
    csv_path = str(os.getcwd()) + "/items_not_logged.csv"
    log = []
    for dir_entry in os.listdir(path):
        temp = []
        dir_entry_path = os.path.join(path, dir_entry)

        if os.path.isdir(dir_entry_path):
            # print dir_entry
            for level_dir in os.listdir(dir_entry_path):
                file_path = os.path.join(dir_entry_path, level_dir)
                # print file_path
                with open(file_path, 'r') as f:
                    d = json.loads(f.read())
                # t = dict()
                name = d.get("name","error")
                utf8_str = name.encode('utf-8')
                name1 = name
                if '\xef' in utf8_str:
                    name2 = re.split('\)', name)
                    name1 = str(name2[0]) + ")"
    
                item_id = d.get("equipment_id","error")
                level = d.get("level","error")
                is_armor = d.get("is_armor",False)
                is_weapon = d.get("is_weapon",False)
                is_upgrade_material = d.get("is_sp_enhancement_material", False)

                if (is_weapon == True or is_armor == True) and (is_upgrade_material == False):

                    base_rarity = d.get("base_rarity","error")
                    # print base_rarity
                    max_evolution_num = d.get("max_evolution_num","error")
                    # print max_evolution_num
                    aa = d["evol_max_level_of_base_rarity"].get(str(base_rarity),"error")
                    # print aa
                    evol_max_level_of_base_rarity = aa.get(str(max_evolution_num),"error")
                    # print evol_max_level_of_base_rarity

                    # print name1 + "," + str(item_id) + " - " + str(base_rarity) + " - " + str(max_evolution_num) + " - " + str(evol_max_level_of_base_rarity)
                    
                    temp.append(level)

            if (is_weapon == True or is_armor == True) and (is_upgrade_material == False):

                base_list = build_max_level_list(evol_max_level_of_base_rarity)

                for p in temp:
                    if p in base_list:
                        base_list.remove(p)
                # print base_list
                if base_list:
                    b = sorted(base_list)
                    q = ""
                    for tt in b:
                        q = str(q) +","+ str(tt)
                    t = {'name': name1, 'id': item_id, 'rarity':base_rarity,'levels': q}
                else:
                    t = {'name': name1, 'id': item_id, 'rarity':base_rarity, 'levels': ",Logged all levels"}
                log.append(t)

    with open(csv_path, 'w') as f:
        for t in log:
            print str(t["name"]) + " " + str(t["id"]) + " - " + str(t["rarity"]) + " - " + str(t["levels"])
            print >> f, str(t["name"]) + "," + str(t["id"]) + str(t["levels"])

    items_not_logged_to_html(log)

def get_recorded_buddy_info_from_csv(file_path):
    entries = []
    for char_file in os.listdir(file_path):
        num_rows = 0
        temp = []
        file_entry_path = os.path.join(file_path, char_file)
        print file_entry_path
        if os.path.isfile(file_entry_path):
            temp = []
            level_rep = []
            levels = []
            fieldnames = ['level', 'hp', 'atk', 'matk', 'acc', 'def', 'mdef', 'eva', 'mnd', 'spd', 'series_level', 'series_hp', 'series_atk', 'series_matk', 'series_acc', 'series_def', 'series_mdef', 'series_eva', 'series_mnd', 'series_spd']
            name = char_file[:-4]
            with open(file_entry_path, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    temp.append(row)
                    num_rows = num_rows + 1

            # convert parameters to ints for sorting
            for p in temp:
                for q in fieldnames:
                    p[q] = int(p[q])

            # temp1 = sorted(temp, key=itemgetter(str(attribute)))
            temp1 = sorted(temp, key=getKey)

            for t in temp1:
                levels.append(int(t["level"]))
            entry = {"name": name, "levels": levels}

        entries.append(entry)
    buddies_not_logged_to_html(entries)


def buddies_not_logged_to_html(log_data):
    log_path = str(os.getcwd()) + "/data/html/buddy_levels.html"
    not_recorded_red = "#F06060"
    recorded_blue = "#30A0B0"
    header_color = "#E0E0E0"


    with open(log_path, 'w') as f:
        print >> f, "<!DOCTYPE html>"
        print >> f, "<html>"
        print >> f, "<body>"
        print >> f, "<table style=\"width:100%\">"
        print >> f, "<tr>"
        print >> f, "<td bgcolor=\"#E0E0E0\">Buddy</td>"
        print >> f, "<td bgcolor=\"#E0E0E0\">Levels</td>"
        
        i = 0
        while i < 65:
            print >> f, "<td bgcolor=\"#E0E0E0\"></td>"
            i += 1

        print >> f, "</tr>"

        for t in log_data:
            print >> f, "<tr>"

            # print >> f, str(t["name"]) + str(t["id"]) + str(t["levels"])
            print >> f, "<td bgcolor=\"#E0E0E0\">" + str(t["name"]) + "</td>"

            j = 1
            while j < 66:
                if j in t["levels"]:
                    print >> f, "<td bgcolor=\"" + recorded_blue + "\">" + str(j) + "</td>"
                else:
                    print >> f, "<td bgcolor=\"" + not_recorded_red + "\">" + str(j) + "</td>"
                j += 1

            print >> f, "</tr>"

        print >> f, "</tr>"
        print >> f, "</table>"
        print >> f, "</body>"
        print >> f, "</html>"

def items_not_logged_to_html(log_data):
    log_path = str(os.getcwd()) + "/data/html/index.html"
    not_recorded_red = "#F06060"
    recorded_blue = "#30A0B0"
    header_color = "#E0E0E0"


    with open(log_path, 'w') as f:
        print >> f, "<!DOCTYPE html>"
        print >> f, "<html>"
        print >> f, "<body>"
        print >> f, "<table style=\"width:100%\">"
        print >> f, "<tr>"
        print >> f, "<td bgcolor=\"#E0E0E0\">Relic</td>"
        print >> f, "<td bgcolor=\"#E0E0E0\">ID</td>"
        print >> f, "<td bgcolor=\"#E0E0E0\">Levels</td>"
        
        i = 0
        while i < 30:
            print >> f, "<td bgcolor=\"#E0E0E0\"></td>"
            i += 1

        print >> f, "</tr>"

        for t in log_data:
            print >> f, "<tr>"

            # print >> f, str(t["name"]) + str(t["id"]) + str(t["levels"])
            print >> f, "<td bgcolor=\"#E0E0E0\">" + str(t["name"]) + "</td>"
            print >> f, "<td bgcolor=\"#E0E0E0\">" + str(t["id"]) + "</td>"

            temp = build_max_level_list(get_item_max_number_of_levels(t["rarity"]))
            # print temp

            if 'L' not in t["levels"][1]:
                c = str(t["levels"][1:]).split(',')
                aa = [] 
                for b in c:
                    aa.append(int(b))
                
                for a in temp:
                    # print a
                    if a in aa:
                        print >> f, "<td bgcolor=\"" + not_recorded_red + "\">" + str(a) + "</td>"
                    else:
                        print >> f, "<td bgcolor=\"" + recorded_blue + "\">" + str(a) + "</td>"
            else:
                for a in temp:
                    print >> f, "<td bgcolor=\"" + recorded_blue + "\">" + str(a) + "</td>"

            print >> f, "</tr>"

        print >> f, "</tr>"
        print >> f, "</table>"
        print >> f, "</body>"
        print >> f, "</html>"


def save_equipment(data):
    for item in data["equipments"]:
        equipment_id = item.get("equipment_id","Error")
        level = item.get("level","0")
        # a = temp_str.replace(" ", "_").lower()
        if not os.access(os.getcwd() + "/data/equipment/" + str(equipment_id) + "/", os.F_OK):
            os.mkdir(os.getcwd() + "/data/equipment/" + str(equipment_id) + "/")

        file_path = "/data/equipment/" + str(equipment_id) + "/" + str(equipment_id) + "_level_" + str(level) + ".json"

        if not os.path.isfile(file_path):
            test_file = open(os.getcwd() + file_path,'w')
            print >> test_file, json.dumps(item, indent=4, sort_keys=True)
            test_file.close()

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

    # only used in mitmdump
    # if ITEMS.get(equipment_id,"Not found") == "Not found":
    #     temp.append([equipment_id, name])
    #     # save_equipment_id(temp)
    #     # print name1
    #     save_equipment_id(equipment_id, name)
    #     # reload dict ITEMS dict?
    #     # doesnt work
    #     # ITEMS = __init__.load_dict("data/items.csv")

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


def sort_item_dict_csv(base_path):

    # used to remove duplicate items and order items by ID/key
    # a = load_dict(base_path + "data/items.csv")
    a = load_dict(os.getcwd() + "/data/items.csv")
    b = a.keys()
    c = sorted(b)
    with open(os.getcwd() + "/data/new_items.csv", 'w') as f:
        for d in c:
            print >> f, str(d) + "," + str(a[d])
            # print str(d) + str(a[d])

def load_battle_init_file():
    battle_init_file = os.getcwd() + "/json/handle_get_battle_init_data.json"
    with open(battle_init_file, 'r') as f:
        data = json.loads(f.read())
    # get_soul_strike_info(data)
    return data

def load_party_list_file():
    buddy_file = os.getcwd() + "/json/handle_party_list.json"
    with open(buddy_file, 'r') as f:
        data = json.loads(f.read())
    # get_buddy_info(data)
    return data

def main():
    # enemy in data - first bracket (start of dict)
    # child in enemy["children"] - array of children dicts
    # drops in child["drop_item_list"] - array of drop dicts

    # data = []
    
    # Don't need to do this if I'm reading/creating new files/folders in mitmdump
    # build_char_data("/data/raw/handle_party_list/")
    # build_char_data("/debug/handle_party_list/")


    build_equipment_stat_file()
    build_buddy_stat_file()

    get_items_not_logged()
    # sort_item_dict_csv("")
    sort_equip_csv_by_attribute("data/csv/equipment/", 'level')
    sort_buddy_csv_by_attribute("data/csv/buddy/", 'level')

    get_recorded_buddy_info_from_csv("data/csv/buddy/")

    # buddy_file = os.getcwd() + "/json/handle_party_list.json"
    # with open(buddy_file, 'r') as f:
    #     data = json.loads(f.read())
    # get_buddy_info(data)

    # battle_init_file = os.getcwd() + "/json/handle_get_battle_init_data.json"
    # with open(battle_init_file, 'r') as f:
    #     data = json.loads(f.read())
    # get_soul_strike_info(data)
    

    # combine_enemy_lists()
    # temp = get_enemy_info()
    # temp2 = get_ability_info("data/abilities.json")
    # print_list_to_file(temp2, "data/abilities_no_duplicates.json")
    # print temp



main()