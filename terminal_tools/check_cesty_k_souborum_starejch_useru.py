#8. 11. jsem se zbavil většiny files-checků co se dělaly furt - buď jsou updatnutý TEĎ nebo sevytvářej s novejma účtama
from pathlib import Path
import json

user_data_folder = Path.cwd().parent / "user_data"

for folder in user_data_folder.iterdir():
    try:
        db_path = folder / "database.json"
        historie_path = folder / "historie_zkouseni.json"
        set_slovicek_path =folder / "set_slovicek.json"
        settings_path = folder / "settings.json"
        for path in [db_path, historie_path, set_slovicek_path]:
            if path.exists():
                pass
            else:
                path.touch()
                with open(path, "w") as file:
                    file.write(json.dumps([]))
        if settings_path.exists():
            pass
        else:
            path.touch()
            with open(settings_path, "w") as file:
                file.write(json.dumps({}))
        
        with open(settings_path) as file:
            s = json.load(file)
        if "jazyky" not in s:
            s["jazyky"] = ["czech","english", "german"]
        if "zkouseni_opakovani" not in s:
            s["zkouseni_opakovani"] = False
        with open(settings_path,"w") as opened:
            opened.write(json.dumps(s))
    except NotADirectoryError: #kvůli DS_store
        pass
