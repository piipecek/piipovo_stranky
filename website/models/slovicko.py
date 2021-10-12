from website.helpers.pretty_date import pretty_date
from website.json_handlers import db_handling
from dateutil import parser
from typing import List
from datetime import datetime

class Slovicko:
    def __init__(self,
                 id: int=None,
                 czech: List[str]=None,
                 german: List[str]=None,
                 english: List[str]=None,
                 druh: List[str]=None,
                 datum=None,
                 asociace: List[str]=None,
                 times_tested: int=0,
                 times_known: int=0,
                 times_learned: int=0,
                 kategorie: List[str]=None):
        if kategorie is None:
            kategorie = ["-"]
        if asociace is None:
            asociace = ["-"]
        if druh is None:
            druh = ["-"]
        if english is None:
            english = ["-"]
        if german is None:
            german = ["-"]
        if czech is None:
            czech = ["-"]
        if datum is None:
            self.datum = str(datetime.utcnow())
        else:
            self.datum = datum
        self.datum_pretty = pretty_date(self.datum)
        self.czech = czech
        self.german = german
        self.english = english
        self.druh = druh
        self.kategorie = kategorie
        self.asociace = asociace
        self.times_tested = times_tested
        self.times_known = times_known
        self.times_learned = times_learned
        self.id = id

    def __repr__(self) -> str:
        return f"CZ: {self.czech} D: {self.german} EN: {self.english}, id: {self.id}, druh: {self.druh}, kategorie: {self.kategorie}, asociace: {self.asociace}, datum: {self.datum}, tested/known: {self.times_tested}/{self.times_known}, learned: {self.times_learned},"

    def json_format(self) -> dict:
        data = {
            "id": self.id,
            "czech": self.czech,
            "german": self.german,
            "english": self.english,
            "druh": self.druh,
            "asociace": self.asociace,
            "times_tested": self.times_tested,
            "times_known": self.times_known,
            "times_learned": self.times_learned,
            "datum": self.datum,
            "kategorie": self.kategorie,
        }
        return data

    def pretty(self, atribute: str) -> str:
        if atribute == "druh":
            return ", ".join(self.druh)
        elif atribute == "asociace":
            return ", ".join(self.asociace)
        elif atribute == "kategorie":
            return ", ".join(self.kategorie)
        elif atribute == "czech":
            return ", ".join(self.czech)
        elif atribute == "english":
            return ", ".join(self.english)
        elif atribute == "german":
            return ", ".join(self.german)
    
    @staticmethod
    def get_by_id(id: int) -> "Slovicko":
        w = db_handling.get_by_id(id)
        if w is None:
            return None
        else:
            return Slovicko(**w)

    def insert_slovicko(self) -> None:
        db_handling.insert_to_db(self.json_format())

    def put_in_db(self) -> None:
        Slovicko.delete_by_id(self.id)
        self.insert_slovicko()

    @staticmethod
    def delete_by_id(id: int):
        db_handling.delete_by_id(id)
    

    @staticmethod
    def get_singles():
        data = db_handling.get_singles_raw()
        if data is None:
            return None
        else:
            result = []
            for word in data:
                result.append(Slovicko.load(word))
            return result
