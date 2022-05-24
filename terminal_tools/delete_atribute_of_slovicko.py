# to be run from console

from json import load, dumps


def del_atribute(name):
    with open("../json_databases/database.json") as file:
        file = load(file)
    for word in file:
        word.pop(name)
    with open("../json_databases/database.json", "w") as database:
        database.write(dumps(file, indent=2))
