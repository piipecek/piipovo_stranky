#what the title says. bylo použito 8. 11. 

from pathlib import Path
import json
user_data_folder = Path.cwd().parent / "user_data"
for folder in user_data_folder.iterdir():
    database_path = folder / "database.json"
    if database_path.exists(): # chrani pred crashem na .DS_store
        with open(database_path) as f:
            f = json.load(f)
        try:
            x = f[0]["v_jazyce"]
        except IndexError:
            break
        except KeyError:
            for word in f:
                v_jazyce = {
                    "czech": word["czech"],
                    "english": word["english"],
                    "german": word["german"]
                }
                word.pop("czech")
                word.pop("english")
                word.pop("german")
                word["v_jazyce"] = v_jazyce
            with open(database_path, "w") as opened:
                opened.write(json.dumps(f, indent=3))
