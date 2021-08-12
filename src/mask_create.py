import labelme
import os, sys

path = "data/jsons/"
dirs = os.listdir(path)
i = 0
for item in dirs:
    if item.endswith(".json"):
        if os.path.isfile(path + item):
            my_dest = "mask_" + str(i)
            os.system("mkdir " + "data/masks/" + my_dest)
            os.system("labelme_json_to_dataset " + (path + item) + " -o " + "data/masks/" + my_dest)
            i = i + 1
