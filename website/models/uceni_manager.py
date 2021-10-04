from warnings import resetwarnings

from flask.helpers import make_response
from website.helpers import set_handling
import random
from website.models.slovicko import Slovicko
from website.helpers.pairser import vyhodnot, smart_sample


class UceniManager:
    def __init__(self, 
                 seznam_dat_slovicek=None, 
                 data_o_uceni=None, 
                 varka=0, 
                 jazyk=None,
                 podle=None,
                 podle_meta=None):
        self.seznam_dat_slovicek = seznam_dat_slovicek
        self.varka = varka
        self.jazyk = jazyk
        self.podle_meta = podle_meta
        self.podle = podle
        if data_o_uceni is None:
            self.data_o_uceni = []
            for date in self.seznam_dat_slovicek:
                self.data_o_uceni.append({
                    "datum": date,
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
            def get_showcase(data_o_uceni):
                kandidati = list(filter(lambda x: x["showcase"] is False, data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    return [zaznam["datum"] for zaznam in smart_sample(kandidati, 4)]

            def get_choose(data_o_uceni):
                kandidati = list(filter(lambda x: x["showcase"] is True and x["choose"] is False, data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    vyvoleny_datum = random.choice(kandidati)["datum"]
                    zaznamy_na_vyber = smart_sample(list(filter(lambda x: x["showcase"] is True and x["datum"] != vyvoleny_datum, data_o_uceni)),3)
                    data_na_vyber = [zaznam["datum"] for zaznam in zaznamy_na_vyber]
                    data_na_vyber.append(vyvoleny_datum)
                    random.shuffle(data_na_vyber)

                    vyvoleny = Slovicko.get_by_timestamp(vyvoleny_datum)
                    slova_na_vyber = [Slovicko.get_by_timestamp(datum) for datum in data_na_vyber]
                    return vyvoleny, slova_na_vyber

            def get_write(data_o_uceni):
                kandidati = list(filter(lambda x: x["showcase"] is True and x["choose"] is True and x["write"] is False,
                                data_o_uceni))
                if len(kandidati) == 0:
                    return None
                else:
                    return random.choice(kandidati)["datum"]

            if self.varka % 9 == 0:
                typ = "showcase"
                datumy_vybranejch = get_showcase(self.data_o_uceni)
                if datumy_vybranejch is None:
                    data_k_odeslani = None
                else:
                    data_k_odeslani = [Slovicko.get_by_timestamp(datum) for datum in datumy_vybranejch]
                    self.sign_as_showcased(datumy_vybranejch)

            elif self.varka % 9 in [1, 2, 3, 4]:
                typ = "choose"
                data_k_odeslani = get_choose(self.data_o_uceni)

            elif self.varka % 9 in [5, 6, 7, 8]:
                typ = "write"
                data_k_odeslani = get_write(self.data_o_uceni)
                if data_k_odeslani is None:
                    data_k_odeslani = None
                else:
                    data_k_odeslani = Slovicko.get_by_timestamp(data_k_odeslani)

            else:
                return "error lol"

            self.varka += 1
            self.zapsat_do_souboru()

            if data_k_odeslani is None:
                return self.get_next_data()
            else:
                return typ, data_k_odeslani

    def sign_as_showcased(self, datumy):
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["datum"] in datumy:
                self.data_o_uceni[i]["showcase"] = True
        self.zapsat_do_souboru()

    def check_choose(self, datum_puvodniho, datum_vybraneho):
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["datum"] == datum_puvodniho:
                if datum_puvodniho == datum_vybraneho:
                    self.data_o_uceni[i]["choose"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["showcase"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_timestamp(datum_puvodniho).pretty(self.jazyk)}"
                    category = "error"
        self.zapsat_do_souboru()
        return message, category

    def check_write(self, datum, string):
        result = vyhodnot(self.jazyk, Slovicko.get_by_timestamp(datum), string)
        for i, zaznam in enumerate(self.data_o_uceni):
            if zaznam["datum"]  == datum:
                if result:
                    self.data_o_uceni[i]["write"] = True
                    message = "Správně!"
                    category = "correct"
                else:
                    self.data_o_uceni[i]["choose"] = False
                    message = f"Špatně, správně by bylo {Slovicko.get_by_timestamp(datum).pretty(self.jazyk)}"
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


