import os
import json
import cv2

import numpy as np

from tqdm import tqdm

data_folder = "data2/jsons/"
dataset_root = "data2/dataset/"

class_list = [
    "blue",
    "gray",
]

files_list = os.listdir(data_folder)
json_list = [x for x in files_list if ".json" in x]

for j in tqdm(json_list):

    orig_image_path = "{}{}.jpeg".format(data_folder, j.split(".")[0])
    orig_image = cv2.imread(orig_image_path)
    orig_image_height, orig_image_width = orig_image.shape[:2]

    mask_image = np.zeros((orig_image_height, orig_image_width, 3), dtype=np.uint8)

    with open("{}{}".format(data_folder, j)) as label_json:
        labels = json.load(label_json)["shapes"]

    for l in labels:
        class_index = class_list.index(l["label"]) + 1
        points = l["points"]

        if l["shape_type"] == "polygon" or l["shape_type"] == "linestrip":
            contour = [np.array(points, dtype=np.int32)]
            cv2.drawContours(mask_image, [contour[0]], 0, (class_index, class_index, class_index), -1)
        elif l["shape_type"] == "rectangle":
            cv2.rectangle(mask_image, (int(points[0][0]), int(points[0][1])), (int(points[1][0]), int(points[1][1])),
                          (class_index, class_index, class_index), -1)

    out_mask_path = "{}annot/{}.png".format(dataset_root, j.split(".")[0])
    out_image_path = "{}img/{}.png".format(dataset_root, j.split(".")[0])

    mask_image =

    cv2.imwrite(out_mask_path, mask_image)
    cv2.imwrite(out_image_path, orig_image)
