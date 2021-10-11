from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models.chyba import Chyba
from website.models.slovnik import Slovnik


default_views = Blueprint("default_views",__name__)


@default_views.route("/")
def restaurant_na_konci_vesmiru():
	return redirect(url_for("default_views.home", current_user=current_user))

@default_views.route("/home")
def home():
	return render_template("home.html", current_user=current_user)


@default_views.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html")

@default_views.route("/known_bugs")
@login_required
def known_bugs():
	chyby  = Chyba.get_all()
	return render_template("zname_chyby.html", chyby=chyby)

@default_views.route("/nahlasit_bug", methods=["GET","POST"])
@login_required
def nahlasit_bug():
	if request.method == "GET":
		return render_template("nahlasit_chybu.html")
	else:
		c = Chyba(
		autor = current_user.email if request.form.get("include_name") else "Anonym",
		popis = request.form.get("popis")
		)
		c.pridat_do_chyb()
		return redirect(url_for("default_views.known_bugs"))

@default_views.route("/planovane_featury")
@login_required
def planovane_featury():
	return render_template("planovane_featury.html")

@default_views.route("/account", methods=["GET","POST"])
@login_required
def account():
	if request.method == "GET":
		s = Slovnik()
		return render_template("account.html", current_user=current_user, pocet_slovicek = len(s.slovicka))
	else:
		return "Not done yet" + request.form.get("uceni_choose")
