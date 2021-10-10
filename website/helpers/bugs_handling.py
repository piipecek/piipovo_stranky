import json
from typing import List
from pathlib import Path

def get_chyby() -> List[dict]:
	c = Path.cwd()
	bugs_path = c / "known_bugs.json"
	if bugs_path.exists():
		pass
	else:
		bugs_path.touch()
		with open(bugs_path, "w") as file:
			file.write(json.dumps([]))

	with open(bugs_path) as file:
		return json.load(file)

def zapsat_do_known_bugs(data):
	with open("known_bugs.json", "w") as file:
		file.write(json.dumps(data, indent=3))

def pridat_do_chyb(data):
	file = get_chyby()
	file.append(data)
	zapsat_do_known_bugs(file)
