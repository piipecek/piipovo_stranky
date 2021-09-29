import json
from flask_login import current_user
from dateutil import parser
from website.helpers.db_handling import sort_slovnik, get_user_database
from website.helpers.pairser import smart_sample

def get_user_set_slovicek():
    with open(f"user_data/{current_user.id}/set_slovicek.json") as file:
        return json.load(file)

def save_to_user_set_slovicek(data):
    with open(f"user_data/{current_user.id}/set_slovicek.json", "w") as file:
        file.write(json.dumps(data, indent=3))


def jazykovej_filtr(jazyk):
    file = get_user_database()
    result = []
    for word in file:
        if (word["czech"] != ["-"]) and (word[jazyk] != ["-"]):
            result.append(word)
    return result


def od_do(od, do, jazyk):
    od = parser.parse(od, dayfirst=False)
    do = parser.parse(do, dayfirst=False)

    file = jazykovej_filtr(jazyk)
    result = []
    for word in file:
        date = parser.parse(word["datum"], dayfirst=True)
        if (date > od) and (date.date() <= do.date()):
            result.append(word)
    return result


def kategorie(katego, jazyk):
    file = jazykovej_filtr(jazyk)
    result = []
    for w in file:
        if katego in w["kategorie"]:
            result.append(w)
    return result


def neuspesnych(kolik, jazyk):
    sort_slovnik(key="neuspesne", sestupne="True")
    file = jazykovej_filtr(jazyk)
    result = []

    for word in file:
        if len(result) == kolik:
            break
        else:
            if word["times_tested"] - word["times_known"] > 0:
                result.append(word)
            else:
                break
    return result


def vse(kolik, jazyk):
    file = jazykovej_filtr(jazyk)
    return smart_sample(file, kolik)


def least(kolik, jazyk):
    sort_slovnik(sestupne=True, key="least")
    file = jazykovej_filtr(jazyk)
    result = []
    nejnizsi_pocet_zkouseni = file[0]["times_tested"]
    for word in file:
        if word["times_tested"] == nejnizsi_pocet_zkouseni:
            result.append(word)
    try:
        result = sample(result, kolik)
    except ValueError:
        result = result
    return result


def druhy(dr, jazyk):
    file = jazykovej_filtr(jazyk)
    result = []
    for w in file:
        if dr in w["druh"]:
            result.append(w)
    return result


def skupina(string, jazyk):
    file = jazykovej_filtr(jazyk)
    result = []
    for w in file:
        for german_w in w["german"]:
            if string in german_w:
                result.append(w)
    return result
