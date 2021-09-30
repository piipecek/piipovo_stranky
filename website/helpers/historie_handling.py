import json
from flask_login import current_user

def get_user_zkouseni_historie():
    with open(f"user_data/{current_user.id}/historie_zkouseni.json") as file:
        return json.load(file)

def save_to_user_zkouseni_historie(data):
    with open(f"user_data/{current_user.id}/historie_zkouseni.json", "w") as file:
        file.write(json.dumps(data, indent=3))


def pridat_zkouseni_do_historie(data):
    file = get_user_zkouseni_historie()
    file.append(data)
    save_to_user_zkouseni_historie(file)
    

def najit_podle_data(date):
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
