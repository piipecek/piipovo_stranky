import json
import website.paths.paths as p
from typing import List


def get_user_zkouseni_historie() -> List[dict]:
    with open(p.user_historie_path()) as file:
        return json.load(file)


def save_to_user_zkouseni_historie(data: list) -> None:
    with open(p.user_historie_path(), "w") as file:
        file.write(json.dumps(data, indent=3))


def pridat_zkouseni_do_historie(data: dict) -> None:
    file = get_user_zkouseni_historie()
    file.append(data)
    save_to_user_zkouseni_historie(file)


def najit_podle_data(date: str) -> None:
    file = get_user_zkouseni_historie()
    for zkouseni in file:
        if zkouseni["datum"] == date:
            return zkouseni


def smazat_podle_data(date):
    file = get_user_zkouseni_historie()
    for i, zkouseni in enumerate(file):
        if zkouseni["datum"] == date:
            file.pop(i)
    save_to_user_zkouseni_historie(file)
