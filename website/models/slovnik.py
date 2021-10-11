from typing import List
from website.models.slovicko import Slovicko
from website.helpers import db_handling

class Slovnik:
    def __init__(self) -> None:
        self.slovicka = [Slovicko(**raw_word) for raw_word in db_handling.get_user_database()]    
    

    def get_next_id(self) -> int:
        id = 0
        for word in self.slovicka:
            if word.id > id:
                id = word.id
        return id + 1


    def json_format(self) -> List[dict]:
        return [word.json_format() for word in self.slovicka]


    """
    def delete_slovicko(self, id: int) -> None:
        for i, word in enumerate(self.slovicka):
            if word.id == id:
                self.slovicka.pop(i)
        db_handling.save_to_user_database(self.json_format())
    """
    def ulozit_do_db(self) -> None:
        db_handling.save_to_user_database(self.json_format())

    
