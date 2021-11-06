from website.models.slovicko import Slovicko
from website.models.slovnik import Slovnik
from website.models.settings import Settings
from random import sample
from typing import Tuple, Sequence


def pairse_cj_x_and_insert(data: str, jazyk: str, asociace: str, druh: str, kategorie: str, obratit: bool) -> Tuple[str]:
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
        if list(line).count("-") == 1:
            continue
        else:
            return line, data


    slovnik = Slovnik.get()

    for line in lines:
        if obratit:
            x, cz = line.split("-")
        else:
            cz, x = line.split("-")

        cz = cz.split(",")
        x = x.split(",")
        while "" in cz:
            cz.remove("")
        while "" in x:
            x.remove("")

        new_word = Slovicko(id=slovnik.get_next_id())
        new_word.v_jazyce["czech"] = cz
        new_word.v_jazyce[jazyk] = x
        new_word.kategorie=kategorie
        new_word.druh=druh
        new_word.asociace=asociace
        slovnik.slovicka.append(new_word)
    slovnik.ulozit_do_db()

        


def vyhodnot(jazyk: str, predloha: Slovicko, string: str) -> bool:
    for j in Settings.get().data["jazyky"]:
        if j == jazyk:
            if string in [p.replace("zde","") for p in predloha.v_jazyce[jazyk]]:
                return True
            else:
                return False

def smart_sample(iterable: Sequence, amount: int) -> list:
    if len(iterable) <= amount:
        return sample(iterable, len(iterable))
    else:
        return sample(iterable, amount)

