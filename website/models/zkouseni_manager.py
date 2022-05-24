from website.helpers.pretty_date import pretty_date
from website.helpers.pairser import vyhodnot
from website.models.slovicko import Slovicko
import random
from datetime import datetime
from website.json_handlers import set_handling
from website.json_handlers import historie_handling
from typing import List, Tuple


class ZkouseniManager:
    def __init__(self,
                 id: int=None,
                 seznam_id_slovicek: list = None,
                 podle: str=None,
                 podle_meta: str=None,
                 datum: str=None,
                 target_jazyk: str=None,
                 base_jazyk: str = None,
                 poznamka: str=None,
                 seznam_odpovedi: List[str]=None,
                 uspesnost: float = None):
        self.seznam_id_slovicek = seznam_id_slovicek
        self.target_jazyk = target_jazyk
        self.base_jazyk = base_jazyk
        self.poznamka = poznamka
        self.podle = podle
        self.podle_meta = podle_meta
        self.uspesnost = uspesnost
        if id is None:
            self.id = ZkouseniManager.get_next_id()
        else:
            self.id = id
        if datum is None:
            self.datum = str(datetime.utcnow())
        else:
            self.datum = datum
        if seznam_odpovedi is None:
            self.seznam_odpovedi = []
        else:
            self.seznam_odpovedi = seznam_odpovedi
        if seznam_id_slovicek is None:
            self.seznam_id_slovicek = []
        else:
            self.seznam_id_slovicek = seznam_id_slovicek

    def pretty_date(self) -> str:
        return pretty_date(self.datum)

    def get_uspesnost(self) -> float:
        seznam_yesno = self.get_seznam_yesno()
        return seznam_yesno.count(1) / len(seznam_yesno)

    def get_seznam_yesno(self) -> List[int]:
        result = []
        for i in range(len(self.seznam_id_slovicek)):
            if vyhodnot(jazyk=self.target_jazyk,
                        predloha=Slovicko.get_by_id(self.seznam_id_slovicek[i]),
                        string=self.seznam_odpovedi[i]):
                result.append(1)
            else:
                result.append(0)
        return result

    def objekty(self) -> List[Slovicko]:
        return Slovicko.get_by_id_list(self.seznam_id_slovicek)

    def zamichat_slovicka(self) -> None:
        random.shuffle(self.seznam_id_slovicek)

    def zapsat_do_souboru(self) -> None:
        result = {
            "id": self.id,
            "target_jazyk": self.target_jazyk,
            "base_jazyk": self.base_jazyk,
            "datum": self.datum,
            "podle": self.podle,
            "podle_meta": self.podle_meta,
            "seznam_id_slovicek": self.seznam_id_slovicek,
            "seznam_odpovedi": self.seznam_odpovedi,
            "poznamka": self.poznamka,
            "uspesnost": self.uspesnost
        }
        set_handling.save_to_user_set_slovicek(result)

    @staticmethod
    def nacist_ze_souboru() -> "ZkouseniManager":
        return ZkouseniManager(**set_handling.get_user_set_slovicek())


    @staticmethod
    def get_next_id() -> int:
        id = 0
        for zaznam in historie_handling.get_user_zkouseni_historie():
            if zaznam["id"] > id:
                id = zaznam["id"]
        return id + 1
        

    def nte_ze_setu(self, n: int) -> Slovicko:
        try:
            return Slovicko.get_by_id(self.seznam_id_slovicek[n])
        except IndexError:
            return False

    def ulozit_do_historie(self) -> None:
        data = {
            "datum": self.datum,
            "podle": self.podle,
            "podle_meta": self.podle_meta,
            "seznam_id_slovicek": self.seznam_id_slovicek,
            "seznam_odpovedi": self.seznam_odpovedi,
            "poznamka": self.poznamka,
            "target_jazyk": self.target_jazyk,
            "base_jazyk": self.base_jazyk,
            "id": self.id,
            "uspesnost": self.get_uspesnost()
        }
        historie_handling.pridat_zkouseni_do_historie(data)

    @staticmethod
    def get_all_from_history() -> List["ZkouseniManager"]:
        data = historie_handling.get_user_zkouseni_historie()
        result = []
        for z in data:
            result.append(ZkouseniManager(**z))
        return result

    @staticmethod
    def get_by_id(id) -> "ZkouseniManager":
        data = historie_handling.najit_podle_id(id)
        obj = ZkouseniManager(**data)
        list_slovicek = Slovicko.get_by_id_list(obj.seznam_id_slovicek)
        old_seznam_id_slovicek = obj.seznam_id_slovicek
        old_seznam_odpovedi = obj.seznam_odpovedi
        obj.seznam_odpovedi = []
        obj.seznam_id_slovicek = []
        for i, slovicko in enumerate(list_slovicek):
            if slovicko is None:
                pass
            else:
                obj.seznam_id_slovicek.append(old_seznam_id_slovicek[i])
                obj.seznam_odpovedi.append(old_seznam_odpovedi[i])
        obj.zapsat_do_souboru
        return obj

    @staticmethod
    def znovu(id: int) -> None:
        z = ZkouseniManager.get_by_id(id)
        z.seznam_odpovedi = []
        z.id = ZkouseniManager.get_next_id()
        z.datum = str(datetime.utcnow())
        z.poznamka += f", přezkoušení z {z.datum}"
        z.zamichat_slovicka()
        z.zapsat_do_souboru()

    @staticmethod
    def delete_by_id(id: int) -> None:
        historie_handling.smazat_podle_id(id)
    

    def nacist_z_dat_o_uceni(self, data_o_uceni: List[dict], podle: str, podle_meta: str) -> None:
        self.podle = podle
        self.podle_meta = podle_meta
        self.poznamka = "Zkoušeno po učení."
        self.seznam_id_slovicek = [zaznam["id"] for zaznam in data_o_uceni]
        self.zapsat_do_souboru()
        



