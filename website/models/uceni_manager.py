from website.helpers import set_handling
import random
from website.models.slovicko import Slovicko
from website.helpers.pairser import vyhodnot, smart_sample


class UceniManager:
    def __init__(self, seznam_dat_slovicek=None, data_o_zkouseni=None, varka=0, jazyk=None):
        self.seznam_dat_slovicek = seznam_dat_slovicek
        self.varka = varka
        self.jazyk = jazyk
        if data_o_zkouseni is None:
            self.data_o_zkouseni = []
            for date in self.seznam_dat_slovicek:
                self.data_o_zkouseni.append({
                    "datum": date,
                    "showcase": False,
                    "choose": False,
                    "write": False
                })
        else:
            self.data_o_zkouseni = data_o_zkouseni
        pass

    def zapsat_do_souboru(self):
        set_handling.save_to_user_set_slovicek(
            {
                "varka": self.varka,
                "jazyk": self.jazyk,
                "data_o_zkouseni": self.data_o_zkouseni
            }
        )

    @staticmethod
    def nacist_ze_souboru():
        data = set_handling.get_user_set_slovicek()
        obj = UceniManager(data_o_zkouseni=data["data_o_zkouseni"],
                           varka=data["varka"],
                           jazyk=data["jazyk"])
        return obj

    def get_next_data(self):
        typ = None
        data_k_odeslani = None

        def get_showcase(data_o_zkouseni):
            kandidati = list(filter(lambda x: x["showcase"] is False, data_o_zkouseni))
            if len(kandidati) == 0:
                return None
            else:
                return [zaznam["datum"] for zaznam in smart_sample(kandidati, 4)]

        def get_choose(data_o_zkouseni):
            kandidati = list(filter(lambda x: x["showcase"] is True and x["choose"] is False, data_o_zkouseni))
            if len(kandidati) == 0:
                return None
            else:
                vyvoleny_datum = random.choice(kandidati)["datum"]
                zaznamy_na_vyber = smart_sample(list(filter(lambda x: x["showcase"] is True and x["datum"] != vyvoleny_datum, data_o_zkouseni)),3)
                data_na_vyber = [zaznam["datum"] for zaznam in zaznamy_na_vyber]
                print("from get_choose, ", data_na_vyber)
                data_na_vyber.append(vyvoleny_datum)
                random.shuffle(data_na_vyber)

                vyvoleny = Slovicko.get_by_timestamp(vyvoleny_datum)
                slova_na_vyber = [Slovicko.get_by_timestamp(datum) for datum in data_na_vyber]
                return vyvoleny, slova_na_vyber

        def get_write(data_o_zkouseni):
            data = list(filter(lambda x: x["showcase"] is True and x["choose"] is True and x["write"] is False,
                               data_o_zkouseni))
            if len(data) == 0:
                return "konec_uceni_trigger"
            else:
                return random.choice(data)["datum"]

        if self.varka == 0:
            typ = "showcase"
            datumy_vybranejch = get_showcase(self.data_o_zkouseni)
            if datumy_vybranejch is None:
                data_k_odeslani = None
            else:
                data_k_odeslani = [Slovicko.get_by_timestamp(datum) for datum in datumy_vybranejch]
                self.sign_as_showcased(datumy_vybranejch)

        elif self.varka in [1, 2]:
            typ = "choose"
            data_k_odeslani = get_choose(self.data_o_zkouseni)
        else:
            rem = (self.varka - 3) % 7
            if rem == 0:
                typ = "showcase"
                datumy_vybranejch = get_showcase(self.data_o_zkouseni)
                if datumy_vybranejch is None:
                    data_k_odeslani = None
                else:
                    data_k_odeslani = [Slovicko.get_by_timestamp(datum) for datum in datumy_vybranejch]
                    self.sign_as_showcased(datumy_vybranejch)
            elif rem in [1, 2, 3]:
                typ = "choose"
                data_k_odeslani = get_choose(self.data_o_zkouseni)
            else:
                typ = "write"
                data_k_odeslani = get_write(self.data_o_zkouseni)
                if data_k_odeslani == "konec_uceni_trigger":
                    pass
                else:
                    data_k_odeslani = Slovicko.get_by_timestamp(data_k_odeslani)

        self.varka += 1
        self.zapsat_do_souboru()

        if data_k_odeslani == "konec_uceni_trigger":
            return None
        elif data_k_odeslani is None:
            return self.get_next_data()
        else:
            return typ, data_k_odeslani

    def check_choose(self, datum_puvodniho, datum_vybraneho):
        if datum_puvodniho == datum_vybraneho:
            for i, zaznam in enumerate(self.data_o_zkouseni):
                if zaznam["datum"] == datum_vybraneho:
                    self.data_o_zkouseni[i]["choose"] = True
        self.zapsat_do_souboru()

    def sign_as_showcased(self, datumy):
        for i, zaznam in enumerate(self.data_o_zkouseni):
            if zaznam["datum"] in datumy:
                self.data_o_zkouseni[i]["showcase"] = True
        self.zapsat_do_souboru()

    def check_write(self, datum, string):
        result = vyhodnot(self.jazyk, Slovicko.get_by_timestamp(datum), string)
        if result:
            for i, zaznam in enumerate(self.data_o_zkouseni):
                if zaznam["datum"] == datum:
                    self.data_o_zkouseni[i]["write"] = True
        self.zapsat_do_souboru()



