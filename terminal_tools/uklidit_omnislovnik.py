from typing import List
import json


def get_pipuv_omnislovnik() -> List[dict]:
    with open("../piipuv_omnislovnik_k_3_10_2021.json") as file:
        file = json.load(file)
    return file


def check_if_slovnik_updated_or_update():
    file = get_pipuv_omnislovnik()
    for word in file:
        word["times_tested"] = 0
        word["times_known"] = 0
        word["times_learned"] = 0
    with open("../piipuv_omnislovnik_k_3_10_2021.json", "w") as opened:
        opened.write(json.dumps(file, indent=3))

# check_if_slovnik_updated_or_update()



def check_update_slovniku_na_jazyky() -> None:
    file = get_pipuv_omnislovnik()
    for zaznam in file:
        zaznam["v_jazyce"] = {}
        zaznam["v_jazyce"]["czech"] = zaznam["czech"]
        zaznam["v_jazyce"]["german"] = zaznam["german"]
        zaznam["v_jazyce"]["english"] = zaznam["english"]
        zaznam.pop("czech")
        zaznam.pop("english")
        zaznam.pop("german")
        
    with open("../piipuv_omnislovnik_k_3_10_2021.json", "w") as opened:
        opened.write(json.dumps(file, indent=3))

#check_update_slovniku_na_jazyky()

def uklidit_pomlcky_a_prazdny_stringy() -> None:
    file = get_pipuv_omnislovnik()
    for word in file:
        def _cleanup_slovo(slovo: list) -> list:
            if "" in slovo:
                slovo.remove("")
            if "-" in slovo:
                slovo.remove("-")
            return slovo
        for jazyk in ["czech", "english", "german"]:
            word["v_jazyce"][jazyk] = _cleanup_slovo(word["v_jazyce"][jazyk])
        word["druh"] = _cleanup_slovo(word["druh"])
        word["kategorie"] = _cleanup_slovo(word["kategorie"])
        word["asociace"] = _cleanup_slovo(word["asociace"])
    with open("../piipuv_omnislovnik_k_3_10_2021.json", "w") as opened:
        opened.write(json.dumps(file, indent=3))

uklidit_pomlcky_a_prazdny_stringy()