from website.json_handlers import settings_handling


class Settings:
    def __init__(self, data: dict = None) -> None:
        if data is None:
            self.data = {
                "zkouseni_opakovani": False
            }
        else:
            self.data = data

    @staticmethod
    def get() -> "Settings":
        got = settings_handling.get_settings()
        if got == []:
            res = Settings()
        else:
            res = Settings(data=got)
        res.save()
        return res
    
    def save(self) -> None:
        return settings_handling.zapsat_do_settings(self.data)
