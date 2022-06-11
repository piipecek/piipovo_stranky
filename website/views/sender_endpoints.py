from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.logs_handling import get_logs
import website.paths.paths as p
from website.models.user import User
from website.paths.paths import multilang_path


sender = Blueprint("sender", __name__)


@sender.route("/send_noauth/<string:query>")
def send_noauth(query):
    if query == "chyby":
        return json.dumps(Chyba.get_all())
    else:
        return f"Query {query} not found."

@sender.route("/send_admin/<string:query>")
def send_admin(query):
    if query == "logs":
        return json.dumps(get_logs())
    elif query == "users_from_data_folder":
        result = []
        for folder in p.user_data_folder_path().iterdir():
            if folder.name == ".DS_Store":
                continue
            else:
                with open(folder / "settings.json") as settings:
                    settings = json.load(settings)
                with open(folder / "database.json") as slovicka:
                    slovicka_count = len(json.load(slovicka))
                result.append({"id": folder.name,
                               "settings": settings,
                               "pocet_slovicek": slovicka_count})
        result.sort(key=lambda x: x["id"])
        return json.dumps(result)
    elif query == "users_from_db":
        return json.dumps([user.get_basic_info() for user in User.query.all()])
    else:
        return "tahle query je nejaka divna."


@sender.route("send_multilang/<string:lang>/<string:location>")
def send_multilang(lang, location) -> str:
    with open(multilang_path()) as file:
        file = json.load(file)

    result = []
    for zaznam in file:
        if zaznam["location"] == location:
            novy_zaznam = {
                "name": zaznam["name"],
            }
            if lang in zaznam["translations"]:
                novy_zaznam["preklad"] = zaznam["translations"][lang]
            else:
                name = zaznam["name"]
                novy_zaznam["preklad"] = f"Tahle kombinace jména a lokace ({name}, {location}) nemá překald pro {lang}."
            result.append(novy_zaznam)

    return json.dumps(result)
    