from website.helpers import set_handling
from website.models.slovicko import Slovicko
from typing import List


class SetSlovicek:
    def __init__(self,
                 podle: str=None,
                 podle_meta: str=None,
                 jazyk: str=None,
                 seznam_id_slovicek: list = None):
        self.podle = podle
        self.podle_meta = podle_meta
        self.jazyk = jazyk
        if seznam_id_slovicek is None:
            self.seznam_id_slovicek = []
        else:
            self.seznam_id_slovicek = seznam_id_slovicek

    def zapsat_do_souboru(self) -> None:
        result = {
            "podle": self.podle,
            "podle_meta": self.podle_meta,
            "jazyk": self.jazyk,
            "seznam_id_slovicek": self.seznam_id_slovicek,
            }

        set_handling.save_to_user_set_slovicek(result)

    @staticmethod
    def nacist_ze_souboru() -> "SetSlovicek":
        return SetSlovicek(**set_handling.get_user_set_slovicek)

    def objekty(self) -> List[Slovicko]:
        return [Slovicko.get_by_id(id) for id in self.seznam_id_slovicek]

    def pripravit_set_od_do(self, od: str, do: str) -> None:
        data = set_handling.od_do(od, do, jazyk=self.jazyk)
        self.podle_meta = (od, do)
        self.nacist_data(data)

    def pripravit_set_kategorie(self, cat: str) -> None:
        data = set_handling.kategorie(cat, jazyk=self.jazyk)
        self.podle_meta = cat
        self.nacist_data(data)

    def pripravit_set_neuspesnych(self, kolik: int) -> None:
        data = set_handling.neuspesnych(kolik, jazyk=self.jazyk)
        self.podle_meta = kolik
        self.nacist_data(data)

    def pripravit_set_vse(self, kolik: int) -> None:
        data = set_handling.vse(kolik, jazyk=self.jazyk)
        self.podle_meta = kolik
        self.nacist_data(data)

    def pripravit_set_least(self, kolik: int) -> None:
        data = set_handling.least(kolik, jazyk=self.jazyk)
        self.podle_meta = kolik
        self.nacist_data(data)

    def pripravit_set_druhy(self, dr: str) -> None:
        data = set_handling.druhy(dr, jazyk=self.jazyk)
        self.podle_meta = dr
        self.nacist_data(data)

    def pripravit_set_skupina(self, string: str) -> None:
        data = set_handling.skupina(string, jazyk=self.jazyk)
        self.podle_meta = string
        self.nacist_data(data)
    
    def pripravit_set_nejmene_ucene(self, kolik: int) -> None:
        data = set_handling.nejmene_ucene(kolik=kolik, jazyk=self.jazyk)
        self.podle_meta = kolik
        self.nacist_data(data)

    def nacist_data(self, data: dict) -> None:
        for word in data:
            self.seznam_id_slovicek.append(word["id"])
        self.zapsat_do_souboru()
