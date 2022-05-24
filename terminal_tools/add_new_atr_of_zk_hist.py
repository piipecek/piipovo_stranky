from json import load, dumps


def new_atribute(name):
    with open("../json_databases/historie_zkouseni.json") as file:
        file = load(file)
    for zaznam in file:
        zaznam[name] = None
    with open("../json_databases/historie_zkouseni.json", "w") as opened:
        opened.write(dumps(file, indent=2))
