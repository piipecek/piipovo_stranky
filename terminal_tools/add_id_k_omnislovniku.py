from typing import List
import json


def get_pipuv_omnislovnik() -> List[dict]:
    with open("../piipuv_omnislovnik_k_3_10_2021.json") as file:
        file = json.load(file)
    return file


def check_if_slovnik_updated_or_update():
    file = get_pipuv_omnislovnik()
    id = 0
    for word in file:
        word["id"] = id
        id += 1
    with open("../omnislovnik_s_id.json", "w") as opened:
        opened.write(json.dumps(file, indent=3))


check_if_slovnik_updated_or_update()
