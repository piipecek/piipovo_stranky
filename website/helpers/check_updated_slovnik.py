import json
from website.json_handlers.db_handling import get_user_database, save_to_user_database
from website.paths.paths import user_historie_path
from website.models.slovnik import Slovnik
from website.models.slovicko import Slovicko

def check_if_slovnik_updated_or_update() -> None:
	file = get_user_database()
	if len(file) == 0:
		print("slovník je prázdnej, takže bude fungovat s novejma ID")
		pass
	else:
		try:
			x = file[0]["id"]
			print("slovník už běží pomocí ID")
		except KeyError:
			print("updatuju slovník na verzi s ID")
			id = 0
			for word in file:
				word["id"] = id
				id += 1
			save_to_user_database(file)

	with open(user_historie_path()) as historie:
		historie = json.load(historie)
	for zaznam in historie:
		try:
			x = zaznam["seznam_id_slovicek"]
		except KeyError:
			print("mazu historii zkouseni protoze i dont care")
			with open(user_historie_path(), "w") as opened:
				opened.write(json.dumps([]))

def check_update_slovniku_na_jazyky() -> None:
	file = get_user_database()
	if len(file) == 0:
		print("slovník je prázdnej, takže bude fungovat s novejma ID")
	else:
		try:
			x = file[0]["v_jazyce"]
		except KeyError:
			s = Slovnik()
			for zaznam in file:
				new_slovicko = Slovicko(id=s.get_next_id())
				new_slovicko.v_jazyce["czech"] = zaznam["czech"]
				new_slovicko.v_jazyce["german"] = zaznam["german"]
				new_slovicko.v_jazyce["english"] = zaznam["english"]
				new_slovicko.druh = zaznam["druh"]
				new_slovicko.asociace = zaznam["asociace"]
				new_slovicko.kategorie = zaznam["kategorie"]
				new_slovicko.times_known= zaznam["times_known"]
				new_slovicko.times_learned = zaznam["times_learned"]
				new_slovicko.times_tested = zaznam["times_tested"]
				new_slovicko.datum = zaznam["datum"]
				s.slovicka.append(new_slovicko)
			s.ulozit_do_db()


