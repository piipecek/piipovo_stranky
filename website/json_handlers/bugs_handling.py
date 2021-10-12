import json
from typing import List
from website.paths.paths import known_bugs_path

def get_chyby() -> List[dict]:
	with open(known_bugs_path()) as file:
		return json.load(file)

def zapsat_do_known_bugs(data) -> None:
	with open(known_bugs_path(), "w") as file:
		file.write(json.dumps(data, indent=3))

def pridat_do_chyb(data: dict) -> None:
	file = get_chyby()
	file.append(data)
	zapsat_do_known_bugs(file)
