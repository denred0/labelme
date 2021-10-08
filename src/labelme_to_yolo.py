import os
import cv2
import json

from tqdm import tqdm

labels_map = {0: 'podnos',}

labelme_dir = "labelme_to_yolo/input/"
darknet_labels = "labelme_to_yolo/output/"

files_list = sorted(os.listdir(labelme_dir))
images_list = [x for x in files_list if ".jpg" in x]

for image in tqdm(images_list):

    img_orig = cv2.imread("{}{}".format(labelme_dir, image))
    cv2.imwrite("labelme_to_yolo/output/" + image, img_orig)

    img_height, img_width = img_orig.shape[:2]

    json_name = "{}.json".format(image.split(".")[0])
    json_path = "{}{}".format(labelme_dir, json_name)

    if json_name not in files_list:

        pass

        with open("{}/{}.txt".format(darknet_labels, image.split(".")[0]), "w") as dl:

            dl.write("")

    else:

        with open(json_path) as j:

            lm_label = json.load(j)

        lm_objects = lm_label["shapes"]

        if len(lm_objects) == 0:
            with open("{}/{}.txt".format(darknet_labels, image.split(".")[0]), "w") as dl:
                dl.write("")

            continue

        for obj in lm_objects:
            points = obj["points"]

            class_id = obj['label']

            if class_id == 'ladle':
                continue

            label = list(labels_map.keys())[list(labels_map.values()).index(obj['label'])]

            xmin = points[0][0]
            ymin = points[0][1]
            xmax = points[1][0]
            ymax = points[1][1]

            rect_width = int(xmax - xmin)
            rect_height = int(ymax - ymin)

            x_center = int(xmin + rect_width / 2)
            y_center = int(ymin + rect_height / 2)

            rel_x_center = min(max(x_center / img_width , 0), 1)
            rel_y_center = min(max(y_center / img_height, 0), 1)
            rel_rect_width = min(max(rect_width / img_width, 0), 1)
            rel_rect_height = min(max(rect_height / img_height, 0), 1)

            with open("{}/{}.txt".format(darknet_labels, image.split(".")[0]), "a") as dl:
                dl.write(
                    "{} {} {} {} {}\n".format(label, rel_x_center, rel_y_center, rel_rect_width, rel_rect_height))
