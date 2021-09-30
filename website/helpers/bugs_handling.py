import json

def get_chyby():
	with open("known_bugs.json") as file:
		return json.load(file)

def zapsat_do_known_bugs(data):
	with open("known_bugs.json", "w") as file:
		file.write(json.dumps(data, indent=3))

def pridat_do_chyb(data):
	file = get_chyby()
	file.append(data)
	zapsat_do_known_bugs(file)
