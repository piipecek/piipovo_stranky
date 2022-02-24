# 7. 11. jsem intreducenul zkouseni z ruznych jazyku, nejen z cestiny -> vedlo to k tomuhle :)
from pathlib import Path
import json
user_data_folder = Path.cwd().parent / "user_data"
for folder in user_data_folder.iterdir():
    historie_file_path = folder / "historie_zkouseni.json"
    if historie_file_path.exists():
        with open(folder / "historie_zkouseni.json", "w") as f:
            f.write(json.dumps([]))