import datetime
from website.models.slovicko import Slovicko
from random import sample


def pairse_cj_x_and_insert(data, jazyk, asociace, druh, kategorie):
    asociace = asociace.replace(", ", ",")
    druh = druh.replace(", ", ",")
    kategorie = kategorie.replace(", ", ",")

    if asociace == "":
        asociace = None
    else:
        asociace = asociace.split(",")
    if druh == "":
        druh = None
    else:
        druh = druh.split(",")
    if kategorie == "":
        kategorie = None
    else:
        kategorie = kategorie.split(",")

    def predpripravit(text):
        text = text.replace("\r", "")
        text = text.replace(" - ", "-")
        text = text.replace("- ", "-")
        text = text.replace(" -", "-")
        text = text.replace(", ", ",")
        text = text.replace(" ,", ",")
        text = text.replace(" , ", ",")
        text = text.replace(": ", ":")
        text = text.replace(" :", ":")
        text = text.replace(" : ", ":")
        text = text.strip()  # removes newlines na konci
        return text

    data = predpripravit(data)
    lines = data.split("\n")
    for line in lines:
        try:
            cz, x = line.split("-")
        except ValueError:
            return False, f"Chyba v zadaném textu, konkrétně na lince: {line}. Na řádku je povolena právě jedna pomlčka.", data
        cz = cz.split(",")
        x = x.split(",")
        while "" in cz:
            cz.remove("")
        while "" in x:
            x.remove("")
        if cz == []:
            cz = ["-"]
        if x == []:
            x = ["-"]

        if jazyk == "english":
            new_word = Slovicko(czech=cz,
                                english=x,
                                kategorie=kategorie,
                                druh=druh,
                                asociace=asociace,
                                datum=str(datetime.datetime.utcnow()))
            new_word.insert_slovicko()
        elif jazyk == "german":
            new_word = Slovicko(czech=cz,
                                german=x,
                                kategorie=kategorie,
                                druh=druh,
                                asociace=asociace,
                                datum=str(datetime.datetime.utcnow()))
            new_word.insert_slovicko()
    return [True]


def vyhodnot(jazyk, predloha, string):
    if jazyk == "german":
        for predloha in predloha.german:
            if string == predloha.replace("zde:", ""):
                return True
            else:
                return False
    elif jazyk == "english":
        for predloha in predloha.english:
            if string == predloha.replace("zde:", ""):
                return True
            else:
                return False


def smart_sample(iterable, amount):
    if len(iterable) <= amount:
        return sample(iterable, len(iterable))
    else:
        return sample(iterable, amount)
