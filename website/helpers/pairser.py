from website.models.slovicko import Slovicko
from website.models.slovnik import Slovnik
from website.models.settings import Settings
from random import sample
from typing import Tuple, Sequence


def pairse_and_insert(data: str, jazyky: list, asociace: str, druh: str, kategorie: str) -> Tuple[str]:
    asociace = asociace.replace(", ", ",")
    druh = druh.replace(", ", ",")
    kategorie = kategorie.replace(", ", ",")

    if asociace == "":
        asociace = []
    else:
        asociace = asociace.split(",")
    if druh == "":
        druh = []
    else:
        druh = druh.split(",")
    if kategorie == "":
        kategorie = []
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
    

    if jazyky.count("") == len(jazyky):
        return "Nevybral jsi žádné jazyky. Zkopíruj si tady svůj vstup a zkus to znova.", data
    while "" == jazyky[-1]:
        jazyky.pop()
    if "" in jazyky:
        return "Nevybral jsi jazyk na pozici, na které jsi psal slovíčka. Zkopíruj si tady svůj vstup a zkus to znova.", data
    if len(list(set(jazyky))) < len(jazyky):
        return "Zvolil jsi některé jazyky 2x. Zkopíruj si tady svůj vstup a zkus to znova.", data

    lines = data.split("\n")
    for line in lines:
        if list(line).count("-")+1 == len(jazyky):
            continue
        else:
            line = "Na řádce " + line + " nesedí počet tebou zadaných jazyků a počet zvolených jazyků k přidávání. Tady si to zkopíruj a zkus to znova."
            return line, data


    slovnik = Slovnik.get()

    for line in lines:
        line = line.split("-")
        for i, elem in enumerate(line):
            line[i] = elem.split(",")
            while "" in line[i]:
                elem.remove("")
        new_word = Slovicko(id=slovnik.get_next_id())
        for tup in zip(jazyky, line):
            new_word.v_jazyce[tup[0]] = tup[1]
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

