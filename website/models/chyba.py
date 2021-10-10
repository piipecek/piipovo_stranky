from website.helpers import bugs_handling
from typing import List


class Chyba:
	def __init__(self, autor, popis, stav="Zatím neřešeno"):
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
	def  get_all() -> List["Chyba"]:
		result = []
		chyby_raw = bugs_handling.get_chyby()
		for chyba in chyby_raw:
			new_obj = Chyba(autor=chyba["autor"],
							popis=chyba["popis"],
							stav=chyba["stav"])
			result.append(new_obj)
		return result
