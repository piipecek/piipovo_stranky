from os import mkdir
import website.paths.paths as p
import json


def check_files_or_create():
    bugs_path = p.known_bugs_path()
    user_folder_path = p.user_folder_path()
    db_path = p.user_database_path()
    historie_path = p.user_historie_path()
    set_slovicek_path = p.user_set_slovicek_path()
    
    if user_folder_path.exists():
        print(str(user_folder_path) + "already exists")
        pass
    else:
        print("creating user folder")
        user_folder_path.mkdir()
    

    for path in [bugs_path, db_path, historie_path, set_slovicek_path]:
        if path.exists():
            print(str(path) + "already exists")
            pass
        else:
            print("creating path " + str(path))
            path.touch()
            with open(path, "w") as file:
                file.write(json.dumps([]))
