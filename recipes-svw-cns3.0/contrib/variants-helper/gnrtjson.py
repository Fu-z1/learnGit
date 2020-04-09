import json
import os
import sys

def load_file(file):

    with open(file, 'r') as f:
        L = json.load(f)
        return L

def get_new_info(list):

    for i in range(0,len(list)):
        dict = {}
        dict["system_variant"] = list[i]["System Variant"]
        dict["variant_info_string"] = list[i]["Variant Info String"]
        list[i] = dict   
    return gnrt_new_dict(list)

def gnrt_new_dict(list):

    new_dict = {}
    new_dict["system_variant"] = list
    new_list = []
    new_list.append(new_dict)
    return new_list

def dump_file(info, file):

    with open(file, 'w') as fw:
        json.dump(info, fw, sort_keys=True, indent=4)

if __name__ == "__main__":

    cwd = sys.path[0]
    root = os.path.join(cwd,'variants-data.json')
    list = load_file(root)
    new_info = get_new_info(list)
    print(new_info)
    #os.system("touch release_info.json")
    dump_file(new_info, "release_info.json")
