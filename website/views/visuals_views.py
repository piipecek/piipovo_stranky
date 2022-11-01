from flask import Blueprint, render_template, send_file, request
from website.paths.paths import hadej_slova_db_path
from tomiem_ipsum.generator import get_tomiem
from catan.catan import generate_catan
from semihra.semihra import generate
from cernabila.cernabila import get_word
import json

visuals_views = Blueprint("visuals_views", __name__)

@visuals_views.route("/rybicky")
def rybicky():
    return render_template("rybicky.html")

@visuals_views.route("/hadej_slova")
def hadej_slova():
    return render_template("hadej_slova.html")


@visuals_views.route("/hadej_slova_getter")
def hadej_slova_getter():
    return send_file(hadej_slova_db_path(), attachment_filename="hadej_slova.json")


@visuals_views.route("/tomiem_ipsum/<int:words>")
def tomiem_ipsum(words):
    return get_tomiem(words=words)

@visuals_views.route("/matematika/popis_primky")
def popis_primky():
    return render_template("popis_primky.html")

@visuals_views.route("/matematika/trig")
def trig():
    return render_template("trig.html")

@visuals_views.route("/matematika/nacrty")
def nacrty():
    return render_template("nacrty.html")

@visuals_views.route("/catan",  methods=["GET","POST"])
def catan():
    if request.method == "GET":
        return render_template("catan.html")
    else:
        got = json.loads(request.form["result"])
        return json.dumps(generate_catan(got))
    

@visuals_views.route("/matlab")
def matlab():
    return render_template("matlab.html")


@visuals_views.route("/semihra", methods=["GET","POST"])
def semihra():
    if request.method == "GET":
        return render_template("semihra.html")
    else:
        jmena = request.form["jmena"]
        indicie =  request.form["indicie"]
        return json.dumps(generate(string_jmen = jmena, string_indicii = indicie))



@visuals_views.route("/frekvence", methods=["GET","POST"])
def frekvence():
    if request.method == "GET":
        return render_template("frekvence.html")
    else:
        return "jeste neumim post"


@visuals_views.route("/cernabila", methods=["GET","POST"])
def cernabila():
    if request.method == "GET":
        return render_template("cernabila.html")
    else:
        return "jeste neumim post"

@visuals_views.route("/cerna_bila_get_word")
def cerna_bila_get_word():
    return json.dumps({"slovo": get_word()})