import json
import labelme
import base64
import cv2
from tqdm import tqdm

from numpy import loadtxt
from pathlib import Path


def get_all_files_in_folder(folder, types):
    files_grabbed = []
    for t in types:
        files_grabbed.extend(folder.rglob(t))
    files_grabbed = sorted(files_grabbed, key=lambda x: x)
    return files_grabbed


# classes_map = {0: "pig", 1: "ladle", 2: "gates", 3: "person", 4: "red_pants", 5: "blue_pants"}
classes_map = {0: "podnos"}

null = None

images = get_all_files_in_folder(Path('../input_yolo'), ['*.jpg'])

for i, img_path in tqdm(enumerate(images), total=len(images)):
    img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]

    # read labels
    lines = loadtxt(str(Path('../input_yolo').joinpath(img_path.stem + '.txt')), delimiter=' ', unpack=False)

    if lines.shape.__len__() == 1:
        lines = [lines]

    cx1y1x2y2 = []
    if len(lines[0]) == 5:
        lines = [[classes_map[int(l[0])], l[1], l[2], l[3], l[4]] for l in lines]

        if i == 254:
            print()

        # convert from yolo to x1, y1, x2, y2

        for l in lines:
            x1 = l[1] * w - l[3] * w / 2
            y1 = l[2] * h - l[4] * h / 2
            x2 = l[1] * w + l[3] * w / 2
            y2 = l[2] * h + l[4] * h / 2

            if x1 < 0: x1 = 0
            if y1 < 0: y1 = 0
            if x2 > w: x2 = w
            if y2 > h: y2 = h
            cx1y1x2y2.append([l[0], x1, y1, x2, y2])

    # create json
    data = {}
    data['version'] = '4.5.7'
    data['flags'] = {}
    data['shapes'] = []
    for l in cx1y1x2y2:
        data['shapes'].append({'label': l[0],
                               'points': [[l[1], l[2]], [l[3], l[4]]],
                               "group_id": null,
                               "shape_type": "rectangle",
                               "flags": {}
                               })
    data['imagePath'] = img_path.name
    data_i = labelme.LabelFile.load_image_file(img_path)
    image_data = base64.b64encode(data_i).decode('utf-8')
    data['imageData'] = image_data
    data['imageHeight'] = h
    data['imageWidth'] = w

    # save json and image
    cv2.imwrite('../output_labelme/' + img_path.name, img)
    if len(cx1y1x2y2) != 0:
        with open('../output_labelme/' + img_path.stem + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
