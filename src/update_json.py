import json
import shutil
import labelme
import base64

from tqdm import tqdm
from pathlib import Path


def get_all_files_in_folder(folder, types):
    files_grabbed = []
    for t in types:
        files_grabbed.extend(folder.rglob(t))
    files_grabbed = sorted(files_grabbed, key=lambda x: x)
    return files_grabbed


null = None

all_images = get_all_files_in_folder(Path('update_json/input'), ['*.jpg'])

for im in tqdm(all_images, desc="Copying images"):
    shutil.copy(im, "update_json/output")

jsons = get_all_files_in_folder(Path('update_json/input'), ['*.json'])
jsons_to_add = get_all_files_in_folder(Path('update_json/input_that_need_add'), ['*.json'])
jsons_to_add_dict = dict(zip([x.stem for x in jsons_to_add], [str(x) for x in jsons_to_add]))

for json_path in tqdm(jsons, desc="Processing jsons"):
    with open(json_path) as j:
        js = json.load(j)

        if json_path.stem in jsons_to_add_dict:
            points_podnos = []

            with open(jsons_to_add_dict[json_path.stem]) as j_add:
                js_add = json.load(j_add)

                lm_objects = js_add["shapes"]

                for obj in lm_objects:
                    points = obj["points"]

                    label = obj['label']

                    xmin = points[0][0]
                    ymin = points[0][1]
                    xmax = points[1][0]
                    ymax = points[1][1]

                    points_podnos.append([label, xmin, ymin, xmax, ymax])

                for p in points_podnos:
                    js['shapes'].append({'label': p[0],
                                         'points': [[p[1], p[2]], [p[3], p[4]]],
                                         "group_id": null,
                                         "shape_type": "rectangle",
                                         "flags": {}
                                         })

                data_i = labelme.LabelFile.load_image_file("update_json/output/" + json_path.stem + ".jpg")
                image_data = base64.b64encode(data_i).decode('utf-8')
                js['imageData'] = image_data

                with open('update_json/output/' + json_path.name, 'w') as outfile:
                    json.dump(js, outfile, indent=2)

        else:
            shutil.copy(json_path, "update_json/output")
            continue

print()
