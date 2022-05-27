from typing import List
from website.json_handlers import bugs_handling


class Chyba:
	def __init__(self, autor: str, popis: str, stav: str = "Zatím neřešeno"):
		self.autor = autor
		self.popis = popis
		self.stav = stav

	def pridat_do_chyb(self) -> None:
		result = {
		"autor": self.autor,
		"popis": self.popis,
		"stav": self.stav
		}
		bugs_handling.pridat_do_chyb(result)

	@staticmethod
	def get_all() -> List[dict]:
		return bugs_handling.get_chyby()
	
	@staticmethod
	def save_po_upravach(data) -> None:
		bugs_handling.zapsat_do_known_bugs(data)
	
	@staticmethod
	def pocet_neresenych() -> int:
		all = Chyba.get_all()
		result = 0
		for chyba in all:
			if chyba["stav"] == "Zatím neřešeno":
				result += 1
		return result