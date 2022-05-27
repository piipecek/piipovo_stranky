from flask import Blueprint
import json
from website.models.chyba import Chyba
from website.json_handlers.logs_handling import get_logs


sender = Blueprint("sender", __name__)


@sender.route("/send_noauth/<string:query>")
def send_noauth(query):
    if query == "chyby":
        return json.dumps(Chyba.get_all())
    else:
        return f"Query {query} not found."

@sender.route("send_admin/<string:query>")
def send_admin(query):
    if query == "logs":
        return json.dumps(get_logs())