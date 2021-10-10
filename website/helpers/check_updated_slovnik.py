from pathlib import Path
import json
from website.helpers.db_handling import get_user_database, save_to_user_database
from flask_login import current_user


def check_if_slovnik_updated_or_update():
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

	with open(f"user_data/{current_user.id}/historie_zkouseni.json") as historie:
		historie = json.load(historie)
	for zaznam in historie:
		try:
			x = zaznam["seznam_id_slovicek"]
		except KeyError:
			print("mazu historii zkouseni protoze i dont care")
			with open(f"user_data/{current_user.id}/historie_zkouseni.json", "w") as opened:
				opened.write(json.dumps([]))