from website.helpers.db_handling import pretty_date
from website.helpers.pairser import vyhodnot
from website.models.slovicko import Slovicko
import random
from datetime import datetime
from website.helpers import set_handling
from website.helpers import historie_handling


class ZkouseniManager:
    def __init__(self,
                 seznam_dat_slovicek: list,
                 podle=None,
                 podle_meta=None,
                 datum=None,
                 jazyk=None,
                 poznamka=None,
                 seznam_odpovedi=None):
        self.seznam_dat_slovicek = seznam_dat_slovicek
        self.jazyk = jazyk
        self.poznamka = poznamka
        self.podle = podle
        self.podle_meta = podle_meta
        if datum is None:
            self.datum = str(datetime.utcnow())
        else:
            self.datum = datum
        if seznam_odpovedi is None:
            self.seznam_odpovedi = []
        else:
            self.seznam_odpovedi = seznam_odpovedi

    def pretty_date(self):
        return pretty_date(self.datum)

    def get_uspesnost(self):
        seznam_yesno = self.get_seznam_yesno()
        return seznam_yesno.count(1) / len(seznam_yesno)

    def get_seznam_yesno(self):
        result = []
        for i in range(len(self.seznam_dat_slovicek)):
            if vyhodnot(jazyk=self.jazyk,
                        predloha=Slovicko.get_by_timestamp(self.seznam_dat_slovicek[i]),
                        string=self.seznam_odpovedi[i]):
                result.append(1)
            else:
                result.append(0)
        return result

    def objekty(self):
        return [Slovicko.get_by_timestamp(date) for date in self.seznam_dat_slovicek]

    def zamichat_slovicka(self):
        random.shuffle(self.seznam_dat_slovicek)

    def zapsat_do_souboru(self):
        result = {
            "jazyk": self.jazyk,
            "datum": self.datum,
            "podle": self.podle,
            "podle_meta": self.podle_meta,
            "seznam_dat_slovicek": self.seznam_dat_slovicek,
            "seznam_odpovedi": self.seznam_odpovedi,
            "poznamka": self.poznamka
        }
        set_handling.save_to_user_set_slovicek(result)

    @staticmethod
    def nacist_ze_souboru():
        data = set_handling.get_user_set_slovicek()
        obj = ZkouseniManager(
            jazyk=data["jazyk"],
            datum=data["datum"],
            podle=data["podle"],
            podle_meta=data["podle_meta"],
            seznam_dat_slovicek=data["seznam_dat_slovicek"],
            seznam_odpovedi=data["seznam_odpovedi"],
            poznamka=data["poznamka"]
        )
        return obj

    def nte_ze_setu(self, n):
        try:
            return Slovicko.get_by_timestamp(self.seznam_dat_slovicek[n])
        except IndexError:
            return False

    def ulozit_do_historie(self):
        data = {
            "datum": self.datum,
            "podle": self.podle,
            "podle_meta": self.podle_meta,
            "seznam_dat_slovicek": self.seznam_dat_slovicek,
            "seznam_odpovedi": self.seznam_odpovedi,
            "poznamka": self.poznamka,
            "jazyk": self.jazyk
        }
        historie_handling.pridat_zkouseni_do_historie(data)

    @staticmethod
    def get_all_from_history():
        data = historie_handling.get_user_zkouseni_historie()
        result = []
        for z in data:
            obj = ZkouseniManager(datum=z["datum"],
                                  podle=z["podle"],
                                  podle_meta=z["podle_meta"],
                                  seznam_dat_slovicek=z["seznam_dat_slovicek"],
                                  seznam_odpovedi=z["seznam_odpovedi"],
                                  poznamka=z["poznamka"],
                                  jazyk=z["jazyk"])
            result.append(obj)
        return result

    @staticmethod
    def get_by_timestamp(timestamp):
        data = historie_handling.najit_podle_data(timestamp)
        message = ""
        obj = ZkouseniManager(datum=data["datum"],
                              podle=data["podle"],
                              podle_meta=data["podle_meta"],
                              seznam_dat_slovicek=data["seznam_dat_slovicek"],
                              seznam_odpovedi=data["seznam_odpovedi"],
                              poznamka=data["poznamka"],
                              jazyk=data["jazyk"])
        for date in obj.seznam_dat_slovicek:
            slovicko = Slovicko.get_by_timestamp(date)
            if slovicko is None:
                obj.seznam_dat_slovicek.pop(date)
                message = "Některá slovíčka chybí, asi byla smazána z databáze."

        return obj, message

    @staticmethod
    def znovu(date):
        z, message = ZkouseniManager.get_by_timestamp(date)
        z.seznam_odpovedi = []
        z.datum = str(datetime.utcnow())
        z.poznamka += f", přezkoušení z {date}"
        z.zapsat_do_souboru()

    @staticmethod
    def delete_by_timestamp(datum):
        historie_handling.smazat_podle_data(datum)


