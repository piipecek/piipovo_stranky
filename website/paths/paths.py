from pathlib import Path
from flask_login import current_user


def known_bugs_path() -> Path:
    cwd = Path.cwd()
    return cwd / "known_bugs.json"


def piipuv_omnislovnik_path() -> Path:
    cwd = Path.cwd()
    return cwd / "piipuv_omnislovnik_k_3_10_2021.json"

def user_data_folder_path() -> Path:
    cwd = Path.cwd()
    return cwd / "user_data"


def user_folder_path() -> Path:
    return user_data_folder_path() / str(current_user.id)


def user_database_path() -> Path:
    return user_folder_path() / "database.json"


def user_historie_path() -> Path:
    return user_folder_path() / "historie_zkouseni.json"


def user_set_slovicek_path() -> Path:
    return user_folder_path() / "set_slovicek.json"


def user_settings_path() -> Path:
    return user_folder_path() / "settings.json"

def hadej_slova_db_path() -> Path:
    return Path.cwd() / "hadej_slova.json"

def tomiem_result_path() -> Path:
    return Path.cwd() / "tomiem_ipsum" / "result.txt"