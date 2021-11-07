from website.json_handlers import set_handling
import random
from website.models.slovicko import Slovicko
from website.helpers.pairser import vyhodnot, smart_sample
from typing import List, Tuple
import math


class UceniManager:
    def __init__(self, 
                 seznam_id_slovicek: list=None, 
                 data_o_uceni: List[dict]=None, 
                 varka: int=0, 
                 target_jazyk: str=None,
                 base_jazyk: str = None,
                 podle: str=None,
                 podle_meta: str=None):
        self.seznam_id_slovicek = seznam_id_slovicek
        self.varka = varka
        self.target_jazyk = target_jazyk
        self.base_jazyk = base_jazyk
        self.podle_meta = podle_meta
        self.podle = podle
        if data_o_uceni is None:
            self.data_o_uceni = []
            for id in self.seznam_id_slovicek:
                self.data_o_uceni.append({
                    "id": id,
                    "showcase": False,
                    "choose": False,
                    "write": False
                })
        else:
            self.data_o_uceni = data_o_uceni

    def zapsat_do_souboru(self) -> None:
        set_handling.save_to_user_set_slovicek(
            {
                "varka": self.varka,
                "target_jazyk": self.target_jazyk,
                "base_jazyk": self.base_jazyk,
                "podle": self.podle,
                "podle_meta": self.podle_meta,
                "data_o_uceni": self.data_o_uceni
            }
        )

    @staticmethod
    def nacist_ze_souboru() -> "UceniManager":
        return UceniManager(**set_handling.get_user_set_slovicek())

    def get_next_data(self):
        typ = None
        data_k_odeslani = None
    
        if all([zaznam["write"] for zaznam in self.data_o_uceni]):
            return None
        else:
            def get_showcase(data_o_uceni: List[dict]) -> List[int]:
                kandidati = list(filter(lambda x: x["showcase"] is False, data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    return [zaznam["id"] for zaznam in smart_sample(kandidati, 4)]

            def get_choose(data_o_uceni: List[dict]) -> Tuple[Slovicko, List[Slovicko]]:
                kandidati = list(filter(lambda x: x["showcase"] is True and x["choose"] is False, data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    vyvoleny_id = random.choice(kandidati)["id"]
                    zaznamy_na_vyber = smart_sample(list(filter(lambda x: x["showcase"] is True and x["id"] != vyvoleny_id, data_o_uceni)),3)
                    id_na_vyber = [zaznam["id"] for zaznam in zaznamy_na_vyber]
                    id_na_vyber.append(vyvoleny_id)
                    random.shuffle(id_na_vyber)

                    vyvoleny = Slovicko.get_by_id(vyvoleny_id)
                    slova_na_vyber = Slovicko.get_by_id_list(id_na_vyber)
                    return vyvoleny, slova_na_vyber

            def get_write(data_o_uceni: List[dict]) -> int:
                kandidati = list(filter(lambda x: x["showcase"] is True and x["choose"] is True and x["write"] is False,
                                data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    return random.choice(kandidati)["id"]

            if self.varka % 9 == 0:
                typ = "showcase"
                id_vybranejch = get_showcase(self.data_o_uceni)
                if id_vybranejch is None:
                    data_k_odeslani = None
                else:
                    data_k_odeslani = Slovicko.get_by_id_list(id_vybranejch)
                    self.sign_as_showcased(id_vybranejch)

            elif self.varka % 9 in [1, 2, 3, 4]:
                typ = "choose"
                data_k_odeslani = get_choose(self.data_o_uceni)

            elif self.varka % 9 in [5, 6, 7, 8]:
                typ = "write"
                data_k_odeslani = get_write(self.data_o_uceni)
                if data_k_odeslani is None:
                    data_k_odeslani = None
                else:
                    data_k_odeslani = Slovicko.get_by_id(data_k_odeslani)

            else:
                return "error lol"

            self.varka += 1
            self.zapsat_do_souboru()

            if data_k_odeslani is None:
                return self.get_next_data()
            else:
                return typ, data_k_odeslani

    def sign_as_showcased(self, ids: List[int]) -> None:
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"] in ids:
                self.data_o_uceni[i]["showcase"] = True
        self.zapsat_do_souboru()

    def get_pocet_written(self) -> Tuple[int, int]:
        pocet_written = 0
        for zaznam in self.data_o_uceni:
            if zaznam["write"] == True:
                pocet_written += 1
        return pocet_written, len(self.data_o_uceni)

    def check_choose(self, id_puvodniho: int, id_vybraneho: int) -> Tuple[str, str]:
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"] == id_puvodniho:
                if id_puvodniho == id_vybraneho:
                    self.data_o_uceni[i]["choose"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["showcase"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_id(id_puvodniho).pretty(self.target_jazyk)}"
                    category = "error"
        self.zapsat_do_souboru()
        return message, category

    def check_write(self, id: int, string: str) -> Tuple[str, str]:
        result = vyhodnot(self.target_jazyk, Slovicko.get_by_id(id), string)
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"]  == id:
                if result:
                    self.data_o_uceni[i]["write"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["choose"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_id(id).pretty(self.target_jazyk)}"
                    category = "error"
        self.zapsat_do_souboru()
        return message, category
    
    def retake(self) -> None:
        for zaznam in self.data_o_uceni:
            zaznam["showcase"] = False
            zaznam["choose"] = False
            zaznam["write"] = False
        self.varka = 0
        self.zapsat_do_souboru()


