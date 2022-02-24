# to be run from console
# potom co tohle probehne, muzu na vsech potrebnych mistech v:
# slovicko.Slovicko
# app.py
# slovnik.html
# edit.html
# implementovat tu novou atribute


from json import load, dumps


def new_atribute(name):
    with open("json_databases/database.json") as file:
        file = load(file)
    for word in file:
        word[name] = 0
    with open("json_databases/database.json", "w") as database:
        database.write(dumps(file, indent=2))
