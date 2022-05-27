import website.paths.paths as p
import json
from website.json_handlers.logs_handling import log


def check_files_or_create() -> None:
    bugs_path = p.known_bugs_path()
    user_data_folder_path = p.user_data_folder_path()
    
    if user_data_folder_path.exists():
        pass
    else:
        user_data_folder_path.mkdir()

    if bugs_path.exists():
        log("Known bugs file already exists.")
    else:
        bugs_path.touch()
        with open(bugs_path, "w") as file:
            file.write(json.dumps([]))
        log("creating Known bugs file at " + str(bugs_path))


def check_logs_file() -> None:
    logs_path = p.log_file_path()
    if logs_path.exists():
        log("(this) log file already exists")
    else:
        print("TOOOOUUCHING")
        logs_path.touch()
        log("creating (this) log file at  " + str(logs_path))

