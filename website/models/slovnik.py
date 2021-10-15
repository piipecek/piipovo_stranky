from typing import List, Dict
from website.models.slovicko import Slovicko
from website.json_handlers import db_handling


class Slovnik:
    def __init__(self) -> None:
        self.slovicka = [Slovicko(**raw_word)
                         for raw_word in db_handling.get_user_database()]

    def get_next_id(self) -> int:
        id = 0
        for word in self.slovicka:
            if word.id > id:
                id = word.id
        return id + 1

    def json_format(self) -> List[dict]:
        return [word.json_format() for word in self.slovicka]

    def delete_slovicko(self, id: int) -> None:
        for i, word in enumerate(self.slovicka):
            if word.id == id:
                self.slovicka.pop(i)
        db_handling.save_to_user_database(self.json_format())

    def ulozit_do_db(self) -> None:
        db_handling.save_to_user_database(self.json_format())

    def get_duplicates(self) -> List[Dict[str,  List[Slovicko]]]:
        vyrazy = []
        duplicitni = {}
        for word in self.slovicka:
            for kolekce in [word.czech, word.english, word.german]:
                for vyraz in kolekce:
                    if vyraz in vyrazy:

                        duplicitni[vyraz].append(word.id)

                    else:
                        vyrazy.append(vyraz)
                        duplicitni[vyraz] = [word.id]
        try:
            duplicitni.pop("-")
        except KeyError:
            pass

        duplicitni_filtered = {}

        for string, ids in duplicitni.items():

            if len(ids) < 2:
                pass
            else:    
                duplicitni_filtered[string] = list(set(ids)) # odebere false duplikaty, kdy je slovo v jednom slovicku ve vice jazycich

        result = []

        # tahle cast je fakt mess
    
        all_potrebny_ids = []
        for strinig, ids in duplicitni_filtered.items():
            all_potrebny_ids += ids
        all_potrebny_ids = list(set(all_potrebny_ids))
        all_potrebny_slovicka = Slovicko.get_by_id_list(all_potrebny_ids)
        dict_potrebnejch_slovicek = {}
        for i, id in enumerate(all_potrebny_ids):
            dict_potrebnejch_slovicek[str(id)] = all_potrebny_slovicka[i]
            
        #

        for string, ids in duplicitni_filtered.items():
            result.append({
                "string": string,
                "words": list(filter(lambda x: x.id in ids, all_potrebny_slovicka))
            })

        if len(result) == 0:
            return None
        else:
            return result

    def sjednotit(self, ids: List[str]) -> None:
        matched_words = Slovicko.get_by_id_list([int(id) for id in ids])
        new = Slovicko(id=self.get_next_id())
        new.datum = matched_words[0].datum 
        for word in matched_words:
            new.czech += word.czech
            new.german += word.german
            new.english += word.english
            new.druh += word.druh
            new.asociace += word.asociace
            new.kategorie += word.kategorie
            new.times_known += word.times_known
            new.times_learned += word.times_learned
            new.times_tested += word.times_tested
            self.delete_slovicko(word.id)
        
        new.czech = list(set(new.czech))
        new.german = list(set(new.german))
        new.english = list(set(new.english))
        new.druh = list(set(new.druh))
        new.asociace = list(set(new.asociace))
        new.kategorie = list(set(new.kategorie))


        self.slovicka.append(new)
        self.ulozit_do_db()

    def natahnout_od_pipa(self, kategorie: list = None):
        piipuv = db_handling.get_pipuv_omnislovnik()

        if kategorie:
            for word in piipuv:
                for one_kat in word["kategorie"]:
                    if one_kat in kategorie:
                        new_slovicko = Slovicko(**word)
                        new_slovicko.id = self.get_next_id()
                        self.slovicka.append(new_slovicko)
        else:
            for word in piipuv:
                new_slovicko = Slovicko(**word)
                new_slovicko.id = self.get_next_id()
                self.slovicka.append(new_slovicko)
        self.ulozit_do_db()

        