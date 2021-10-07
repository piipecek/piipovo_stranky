import typing
from website.helpers import set_handling
import random
from website.models.slovicko import Slovicko
from website.helpers.pairser import vyhodnot, smart_sample
from typing import List, Tuple


class UceniManager:
    def __init__(self, 
                 seznam_id_slovicek=None, 
                 data_o_uceni=None, 
                 varka=0, 
                 jazyk=None,
                 podle=None,
                 podle_meta=None):
        self.seznam_id_slovicek = seznam_id_slovicek
        self.varka = varka
        self.jazyk = jazyk
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
        pass

    def zapsat_do_souboru(self):
        set_handling.save_to_user_set_slovicek(
            {
                "varka": self.varka,
                "jazyk": self.jazyk,
                "podle": self.podle,
                "podle_meta": self.podle_meta,
                "data_o_uceni": self.data_o_uceni
            }
        )

    @staticmethod
    def nacist_ze_souboru():
        data = set_handling.get_user_set_slovicek()
        obj = UceniManager(data_o_uceni=data["data_o_uceni"],
                           varka=data["varka"],
                           jazyk=data["jazyk"],
                           podle=data["podle"],
                           podle_meta=data["podle_meta"])
        return obj

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
                    slova_na_vyber = [Slovicko.get_by_id(id) for id in id_na_vyber]
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
                    data_k_odeslani = [Slovicko.get_by_id(id) for id in id_vybranejch]
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

    def sign_as_showcased(self, ids):
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"] in ids:
                self.data_o_uceni[i]["showcase"] = True
        self.zapsat_do_souboru()

    def check_choose(self, id_puvodniho: int, id_vybraneho: int):
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"] == id_puvodniho:
                if id_puvodniho == id_vybraneho:
                    self.data_o_uceni[i]["choose"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["showcase"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_id(id_puvodniho).pretty(self.jazyk)}"
                    category = "error"
        self.zapsat_do_souboru()
        return message, category

    def check_write(self, id: int, string: str):
        result = vyhodnot(self.jazyk, Slovicko.get_by_id(id), string)
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["id"]  == id:
                if result:
                    self.data_o_uceni[i]["write"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["choose"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_id(id).pretty(self.jazyk)}"
                    category = "error"
        self.zapsat_do_souboru()
        return message, category
    
    def retake(self):
        for zaznam in self.data_o_uceni:
            zaznam["showcase"] = False
            zaznam["choose"] = False
            zaznam["write"] = False
        self.varka = 0
        self.zapsat_do_souboru()


