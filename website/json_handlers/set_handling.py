import json
from dateutil import parser
from website.json_handlers.db_handling import sort_slovnik, jazykovej_filtr
from website.helpers.pairser import smart_sample
import website.paths.paths as p
from typing import List

def get_user_set_slovicek() -> dict:
    with open(p.user_set_slovicek_path()) as file:
        return json.load(file)

def save_to_user_set_slovicek(data: dict) -> None:
    with open(p.user_set_slovicek_path(), "w") as file:
        file.write(json.dumps(data, indent=3))


def od_do(od: str, do:str, target_jazyk:str, base_jazyk: str) -> List[dict]:
    od = parser.parse(od, dayfirst=False)
    do = parser.parse(do, dayfirst=False)

    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    for word in file:
        date = parser.parse(word["datum"], dayfirst=True)
        if (date > od) and (date.date() <= do.date()):
            result.append(word)
    return result


def kategorie(katego: str, target_jazyk: str, base_jazyk: str) -> List[dict]:
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    for w in file:
        if katego in w["kategorie"]:
            result.append(w)
    return result


def neuspesnych(kolik: int, target_jazyk: str, base_jazyk: str) -> List[dict]:
    sort_slovnik(key="neuspesne", sestupne=True)
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []

    if len(file)<=kolik:
        result = file
    else:
        for i in range(kolik):
            result.append(file[i])
    return result


def vse(kolik: int, target_jazyk: str, base_jazyk: str) -> List[dict]:
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    return smart_sample(file, kolik)


def least(kolik: int, target_jazyk: str, base_jazyk: str) -> List[dict]:
    sort_slovnik(sestupne=False, key="least")
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    if len(file) <= kolik:
        result = file
    else:
        for i in range(kolik):
            result.append(file[i])
    return result


def druhy(dr: str, target_jazyk: str, base_jazyk: str) -> List[dict]:
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    for w in file:
        if dr in w["druh"]:
            result.append(w)
    return result


def skupina(string: str, target_jazyk: str, base_jazyk: str) -> List[dict]:
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    for w in file:
        for single_word in w["v_jazyce"][target_jazyk]:
            if string in single_word:
                result.append(w)
    return result

def nejmene_ucene(kolik: int, target_jazyk: str, base_jazyk: str) -> List[dict]:
    sort_slovnik(sestupne=False, key="nejmene_ucene")
    file = jazykovej_filtr(base_jazyk = base_jazyk, target_jazyk = target_jazyk)
    result = []
    if len(file) <= kolik:
        result = file
    else:
        for i in range(kolik):
            result.append(file[i])
    return result
