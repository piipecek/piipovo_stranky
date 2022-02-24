# 8. 11. jsem odebral "" a "-" ze všech slovníků a odebral opakovaný uklízení slovníků
from pathlib import Path
import json

user_data_folder = Path.cwd().parent / "user_data"
for folder in user_data_folder.iterdir():
    database_path = folder / "database.json"
    if database_path.exists(): # chrani pred crashem na .DS_store
        with open(database_path) as f:
            f = json.load(f)
        for word in f:
            for parazit in ["","-"]:
                while parazit in word["kategorie"]:
                    word["kategorie"].remove(parazit)
                while parazit in word["asociace"]:
                    word["asociace"].remove(parazit)
                while parazit in word["druh"]:
                    word["druh"].remove(parazit)
                for zaznam in word["v_jazyce"]:
                    while parazit in word["v_jazyce"][zaznam]:
                        word["v_jazyce"][zaznam].remove(parazit)
        with open(database_path, "w") as opened:
            opened.write(json.dumps(f, indent=3))