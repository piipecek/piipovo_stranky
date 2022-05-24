#update z 9. 11. zavinil, ze pri nevyplneni druhu pri pridavbani slovicek byl null misto []. to musim opravit


from pathlib import Path
import json
user_data_folder = Path.cwd().parent / "user_data"
for folder in user_data_folder.iterdir():
    database_path = folder / "database.json"
    if database_path.exists(): # chrani pred crashem na .DS_store
        with open(database_path) as f:
            f = json.load(f)
        for zaznam in f:
            if zaznam["druh"] is None:
                zaznam["druh"] = []
            if zaznam["asociace"] is None:
                zaznam["asociace"] = []
            if zaznam["kategorie"] is None:
                zaznam["kategorie"] = []
        with open(database_path, "w") as opened:
            opened.write(json.dumps(f, indent=3))
