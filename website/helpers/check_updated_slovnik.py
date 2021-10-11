import json
from website.helpers.db_handling import get_user_database, save_to_user_database
from website.paths.paths import user_historie_path

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