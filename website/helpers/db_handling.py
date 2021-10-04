import json
from types import resolve_bases
from dateutil import parser
from flask_login import current_user
from typing import List

def get_user_database() -> List[dict]:
    with open(f"user_data/{current_user.id}/database.json") as file:
        file = json.load(file)
    return file

def save_to_user_database(data: dict) -> None:
    with open(f"user_data/{current_user.id}/database.json", "w") as file:
        file.write(json.dumps(data, indent=3))

def get_pipuv_omnislovnik() -> List[dict]:
    with open("piipuv_omnislovnik_k_3_10_2021.json") as file:
        file = json.load(file)
    return file


def pretty_date(date):
    date, time = date.split(" ")
    year, month, day = date.split("-")
    time, milis = time.split(".")
    hour, minute, sec = time.split(":")
    return f"{day}. {month}. {year}, {hour}:{minute}:{sec}"


def insert_to_db(data):
    file = get_user_database()
    file.append(data)
    save_to_user_database(file)


def get_all_raw():
    return get_user_database()


def get_by_timestamp_raw(date):
    file = get_user_database()
    for word in file:
        if parser.parse(word["datum"], dayfirst=True) == parser.parse(date, dayfirst=True):
            return word
    return None


def delete_by_date(date):
    file = get_user_database()
    for i, word in enumerate(file):
        if parser.parse(word["datum"], dayfirst=True) == parser.parse(date, dayfirst=True):
            file.pop(i)
    save_to_user_database(file)


def sort_slovnik(key, sestupne):
    file = get_user_database()
    if sestupne == "True":
        rev = True
    else:
        rev = False
    if key == "datum" or key == "druh":
        file.sort(reverse=rev, key=lambda word: word[key])
    elif key == "czech" or key == "kategorie":
        file.sort(reverse=rev, key=lambda word: word[key][0])
    elif key == "neuspesne":
        file.sort(reverse=rev, key=lambda word: word["times_tested"]-word["times_known"])
    elif key == "least":
        file.sort(reverse=rev, key=lambda word: word["times_tested"])
    elif key == "nejmene_ucene":
        file.sort(reverse=rev, key=lambda word: word["times_learned"])

    save_to_user_database(file)


def get_kategorie(jazyk=None):
    file = get_user_database()
    kat = []
    if jazyk is None:
        for word in file:
            for one_kat in word["kategorie"]:
                if one_kat in kat:
                    continue
                else:
                    kat.append(one_kat)
    else:
        for word in file:
            if word[jazyk] != ["-"]:
                for one_kat in word["kategorie"]:
                    if one_kat in kat:
                        continue
                    else:
                        kat.append(one_kat)
    return kat


def get_druhy(jazyk):
    file = get_user_database()
    dr = []
    for word in file:
        if word[jazyk] != ["-"]:
            for one_dr in word["druh"]:
                if one_dr in dr:
                    continue
                else:
                    dr.append(one_dr)
    return dr


def get_singles_raw():
    file = get_user_database()
    result = []
    for word in file:
        count = 0
        if word["czech"] == ["-"]:
            count += 1
        if word["german"] == ["-"]:
            count += 1
        if word["english"] == ["-"]:
            count += 1
        if count == 2:
            result.append(word)
    if len(result) == 0:
        return None
    else:
        return result


def get_duplicates_raw():
    file = get_user_database()
    result = []
    ceska_slova = []
    anglicka_slova = []
    nemecka_slova = []
    duplicitni_vyrazy = []  # pro chytani trojitejch a vice

    for word in file:  # jednou to projede a najde vyrazy, podruhy to nahazi ty slova
        if word["czech"] != ["-"]:
            for vyraz in word["czech"]:
                if vyraz in ceska_slova:
                    if vyraz not in duplicitni_vyrazy:
                        duplicitni_vyrazy.append(vyraz)
                        result.append(
                            {
                                "string": vyraz,
                                "slova": []
                            }
                        )
                else:
                    ceska_slova.append(vyraz)

        if word["german"] != ["-"]:
            for vyraz in word["german"]:
                if vyraz in nemecka_slova:
                    if vyraz not in duplicitni_vyrazy:
                        duplicitni_vyrazy.append(vyraz)
                        result.append(
                            {
                                "string": vyraz,
                                "slova": []
                            }
                        )
                else:
                    nemecka_slova.append(vyraz)

        if word["english"] != ["-"]:
            for vyraz in word["english"]:
                if vyraz in anglicka_slova:
                    if vyraz not in duplicitni_vyrazy:
                        duplicitni_vyrazy.append(vyraz)
                        result.append(
                            {
                                "string": vyraz,
                                "slova": []
                            }
                        )
                else:
                    anglicka_slova.append(vyraz)
    for word in file:
        for vyraz in word["czech"]:
            if vyraz in duplicitni_vyrazy:
                for zaznam in result:
                    if zaznam["string"] == vyraz:
                        zaznam["slova"].append(word)
        for vyraz in word["german"]:
            if vyraz in duplicitni_vyrazy:
                for zaznam in result:
                    if zaznam["string"] == vyraz:
                        zaznam["slova"].append(word)

        for vyraz in word["english"]:

            if vyraz in duplicitni_vyrazy:
                for zaznam in result:
                    if zaznam["string"] == vyraz:
                        zaznam["slova"].append(word)
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

def natahnout_od_pipa(kategorie: list = None) -> None:
    piipuv_omnislovnik = get_pipuv_omnislovnik()
    user_slovnik = get_user_database()
    for word in piipuv_omnislovnik:
        word["times_tested"] = 0
        word["times_known"] = 0
        word["times_learned"] = 0

    if kategorie is None:
        save_to_user_database(user_slovnik + piipuv_omnislovnik)
    else:
        result = []
        for word in piipuv_omnislovnik:
            for one_kat in word["kategorie"]:
                if one_kat in kategorie:
                    result.append(word)
        save_to_user_database(user_slovnik + result)

