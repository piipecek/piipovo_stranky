import json
from typing import List
import website.paths.paths as p

def get_user_database() -> List[dict]:
    with open(p.user_database_path()) as file:
        file = json.load(file)
    return file

def save_to_user_database(data: List[dict]) -> None:
    with open(p.user_database_path(), "w") as file:
        file.write(json.dumps(data, indent=3))

def get_pipuv_omnislovnik() -> List[dict]:
    with open(p.piipuv_omnislovnik_path()) as file:
        file = json.load(file)
    return file


def insert_to_db(data: dict):
    file = get_user_database()
    file.append(data)
    save_to_user_database(file)


def get_by_id(id: int) -> dict:
    file = get_user_database()
    for word in file:
        if word["id"] == id:
            return word

def get_by_ids_list(ids: List[int])  -> List[dict]:
    file = get_user_database()
    result = []
    for word in file:
        if word["id"] in ids:
            result.append(word)
    result_sorted =[]
    for id in ids:
        result_sorted.append(next(filter(lambda x: x["id"] == id,result), None)) # append jediny vysledek filteru, proto next()
    return result_sorted

def delete_by_id(id: int) -> None:
    file = get_user_database()
    for i, word in enumerate(file):
        if word["id"] == id:
            file.pop(i)
    save_to_user_database(file)


def sort_slovnik(key: str, sestupne: bool):
    file = get_user_database()
    if key == "datum" or key == "druh":
        file.sort(reverse=sestupne, key=lambda word: word[key])
    elif key == "kategorie":
        file.sort(reverse=sestupne, key=lambda word: word[key][0])
    elif key == "czech":
        file.sort(reverse=sestupne, key=lambda word: word["v_jazyce"][key][0])
    elif key == "neuspesne":
        file.sort(reverse=sestupne, key=lambda word: word["times_tested"]-word["times_known"])
    elif key == "least":
        file.sort(reverse=sestupne, key=lambda word: word["times_tested"])
    elif key == "nejmene_ucene":
        file.sort(reverse=sestupne, key=lambda word: word["times_learned"])

    save_to_user_database(file)

def jazykovej_filtr(jazyk: str) -> List[dict]:
    file = get_user_database()
    result = []
    for word in file:
        if (word["v_jazyce"]["czech"] != []) and (word["v_jazyce"][jazyk] != []):
            result.append(word)
    return result


def get_kategorie(jazyk: str=None) -> List[str]:
    kat = []
    if jazyk is None:
        file = get_user_database()
        for word in file:
            for one_kat in word["kategorie"]:
                if one_kat in kat:
                    continue
                else:
                    kat.append(one_kat)
    else:
        file = jazykovej_filtr(jazyk)
        for word in file:
            for one_kat in word["kategorie"]:
                if one_kat in kat:
                    continue
                else:
                    kat.append(one_kat)
    return kat


def get_druhy(jazyk: str) -> List[str]:
    file = get_user_database()
    dr = []
    for word in file:
        if word["v_jazyce"][jazyk] != ["-"]:
            for one_dr in word["druh"]:
                if one_dr in dr:
                    continue
                else:
                    dr.append(one_dr)
    return dr


def get_singles_raw():
    from website.models.settings import Settings
    file = get_user_database()
    result = []
    for word in file:
        count = 0
        for jazyk in Settings.get().data["jazyky"]:
            if word["v_jazyce"][jazyk] != []:
                count += 1
        if count == 1:
            result.append(word)
    if len(result) == 0:
        return None
    else:
        return result
        

def get_kategorie_od_piipa() -> List[str]:
    result = []
    for word in get_pipuv_omnislovnik():
        for one_kat in word["kategorie"]:
            if one_kat in result:
                pass
            else:
                result.append(one_kat)
    return result
