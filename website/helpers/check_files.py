import website.paths.paths as p
import json


def check_files_or_create() -> None:
    bugs_path = p.known_bugs_path()
    user_data_folder_path = p.user_data_folder_path()
    
    if user_data_folder_path.exists():
        pass
    else:
        user_data_folder_path.mkdir()

    if bugs_path.exists():
        pass
    bugs_path.touch()
    with open(bugs_path, "w") as file:
        file.write(json.dumps([]))
