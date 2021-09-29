from website.helpers import db_handling
from dateutil import parser


class Slovicko:
    def __init__(self,
                 czech=None,
                 german=None,
                 english=None,
                 druh=None,
                 datum=None,
                 asociace=None,
                 times_tested=0,
                 times_known=0,
                 times_learned=0,
                 kategorie=None):
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
            self.datum = "-"
            self.datum_pretty = "-"
        else:
            self.datum = datum
            self.datum_pretty = db_handling.pretty_date(datum)
        self.czech = czech
        self.german = german
        self.english = english
        self.druh = druh
        self.kategorie = kategorie
        self.asociace = asociace
        self.times_tested = times_tested
        self.times_known = times_known
        self.times_learned = times_learned

    def __repr__(self):
        return f"CZ: {self.czech} D: {self.german} EN: {self.english}, \n," \
               f"druh: {self.druh}, kategorie: {self.kategorie}, asociace: {self.asociace}, \n," \
               f"datum: {self.datum}, tested/known: {self.times_tested}/{self.times_known}, " \
               f"learned: {self.times_learned},"

    def json_format(self):
        data = {
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

    def pretty(self, atribute):
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

    def insert_slovicko(self):
        db_handling.insert_to_db(self.json_format())

    def put_in_db(self, old_date):
        Slovicko.delete_by_timestamp(old_date)
        self.insert_slovicko()

    @staticmethod
    def get_by_timestamp(date):
        w = db_handling.get_by_timestamp_raw(date)
        if w is None:
            return None
        else:
            obj = Slovicko.load(w)
            return obj

    @staticmethod
    def delete_by_timestamp(date):
        db_handling.delete_by_date(date)


    @staticmethod
    def get_all():
        result = []
        data = db_handling.get_all_raw()
        for word in data:
            obj = Slovicko.load(word)
            result.append(obj)
        return result

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

    @staticmethod
    def get_duplicates():
        data = db_handling.get_duplicates_raw()
        if data is None:
            return None
        else:
            result = []
            for zaznam in data:
                new_zaznam = {
                        "string": zaznam["string"],
                        "slova": []
                    }
                for slovo in zaznam["slova"]:
                    new_zaznam["slova"].append(Slovicko.load(slovo))
                result.append(new_zaznam)
            return result

    @staticmethod
    def load(data_z_db):
        d = data_z_db  # pro psani min znaku
        obj = Slovicko(czech=d["czech"],
                       german=d["german"],
                       english=d["english"],
                       druh=d["druh"],
                       asociace=d["asociace"],
                       kategorie=d["kategorie"],
                       datum=d["datum"],
                       times_known=d["times_known"],
                       times_tested=d["times_tested"],
                       times_learned=d["times_learned"])
        return obj

    @staticmethod
    def sjednotit_dve(dat1, dat2):
        obj1 = Slovicko.get_by_timestamp(dat1)
        obj2 = Slovicko.get_by_timestamp(dat2)

        new_datum = str(max(
            parser.parse(obj1.datum, dayfirst=True),
            parser.parse(obj2.datum, dayfirst=True)
        ))

        new_obj = Slovicko(
            czech=obj1.czech,
            german=obj1.german,
            english=obj1.english,
            druh=obj1.druh,
            asociace=obj1.asociace,
            kategorie=obj1.kategorie,
            datum=new_datum
        )

        for vyraz in obj2.czech:
            if vyraz not in new_obj.czech:
                new_obj.czech.append(vyraz)
        for vyraz in obj2.german:
            if vyraz not in new_obj.german:
                new_obj.german.append(vyraz)
        for vyraz in obj2.english:
            if vyraz not in new_obj.english:
                new_obj.english.append(vyraz)
        for vyraz in obj2.druh:
            if vyraz not in new_obj.druh:
                new_obj.druh.append(vyraz)
        for vyraz in obj2.asociace:
            if vyraz not in new_obj.asociace:
                new_obj.asociace.append(vyraz)
        for vyraz in obj2.kategorie:
            if vyraz not in new_obj.kategorie:
                new_obj.kategorie.append(vyraz)

        new_obj.times_tested = obj1.times_tested + obj2.times_tested
        new_obj.times_known = obj1.times_known + obj2.times_known
        new_obj.times_learned =obj1.times_learned + obj2.times_learned

        Slovicko.delete_by_timestamp(dat1)
        Slovicko.delete_by_timestamp(dat2)
        new_obj.insert_slovicko()

