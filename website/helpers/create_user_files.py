import website.paths.paths as p
import json

def create_user_files()-> None:
    p.user_folder_path().mkdir()
    for path in [p.user_database_path(), p.user_historie_path(), p.user_set_slovicek_path()]:
            path.touch()
            with open(path, "w") as file:
                file.write(json.dumps([]))


    p.user_settings_path().touch()
    default = {
        "jazyky": [],
        "zkouseni_opakovani": False
    }
    with open(p.user_settings_path(), "w") as file:
        file.write(json.dumps(default))