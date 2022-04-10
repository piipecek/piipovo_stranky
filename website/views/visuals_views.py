from flask import Blueprint, render_template, send_file
from website.paths.paths import hadej_slova_db_path
from tomiem_ipsum.generator import get_tomiem
from flask_cors import cross_origin

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
#@cross_origin()
def tomiem_ipsum(words):
    return get_tomiem(words=words)

@visuals_views.route("/numerika")
def numerika():
    return render_template("numerika.html")