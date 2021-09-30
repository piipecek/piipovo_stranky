from pathlib import Path
import json


def check_user_slovnik_or_create(user):
	cwd = Path.cwd()
	user_data_path = cwd / "user_data"
	p = user_data_path / f"{user.id}"


	if p.exists():
		print("This user already has initialised Slovnik, so I am not creating new files in userdata")
		pass
	else:
		print("This user used Slovnik for the first time, generating files.")
		database_path = p / "database.json"
		historie_path = p / "historie_zkouseni.json"
		set_slovicek_path = p / "set_slovicek.json"

		p.mkdir()

		database_path.touch()
		historie_path.touch()
		set_slovicek_path.touch()

		with open(database_path,"w") as file:
			file.write(json.dumps([]))
		with open(historie_path, "w") as file:
			file.write(json.dumps([]))
		with open(set_slovicek_path, "w") as file:
			file.write(json.dumps({}))



