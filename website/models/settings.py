from website.json_handlers import settings_handling
from typing import List
from website.json_handlers.db_handling import get_user_database, save_to_user_database


class Settings:
    def __init__(self, data: dict = None) -> None:
        if data is None:
            self.data = {}
        else:
            self.data = data

    def check_format(self) -> None: 
        if "jazyky" not in self.data:
            self.data["jazyky"] = ["czech","english", "german"]
        if "zkouseni_opakovani" not in self.data:
            self.data["zkouseni_opakovani"] = False
        self.save()

    @staticmethod
    def get() -> "Settings":
        got = settings_handling.get_settings()
        if got == []:
            res = Settings()
        else:
            res = Settings(data=got)
        return res
    
    def pretty_jazyky(self):
        return ", ".join(self.data["jazyky"])
    
    def get_jazyky(self) -> List[str]:
        return self.data["jazyky"]
    
    def add_jazyk(self, jazyk:str) -> None:
        jazyky = jazyk.replace(", ",",").split(",")
        file = get_user_database()
        for j in jazyky:
            if j not in self.data["jazyky"]:
                self.data["jazyky"].append(j)
                for word in file:
                    word["v_jazyce"][j] = []
        save_to_user_database(file)
        self.save()
    
    def save(self) -> None:
        return settings_handling.zapsat_do_settings(self.data)
