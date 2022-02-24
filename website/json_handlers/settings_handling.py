import json
from website.paths.paths import user_settings_path

def get_settings() -> dict:
	with open(user_settings_path()) as file:
		return json.load(file)

def zapsat_do_settings(data) -> None:
	with open(user_settings_path(), "w") as file:
		file.write(json.dumps(data, indent=3))