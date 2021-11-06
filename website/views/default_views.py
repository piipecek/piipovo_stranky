from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models.chyba import Chyba
from website.models.slovnik import Slovnik
from website.models.settings import Settings


default_views = Blueprint("default_views",__name__)


@default_views.route("/")
def restaurant_na_konci_vesmiru():
	return redirect(url_for("default_views.dashboard", current_user=current_user))

@default_views.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@default_views.route("/known_bugs")
def known_bugs():
	chyby  = Chyba.get_all()
	return render_template("zname_chyby.html", chyby=chyby)

@default_views.route("/nahlasit_bug", methods=["GET","POST"])
def nahlasit_bug():
	if request.method == "GET":
		return render_template("nahlasit_chybu.html")
	else:
		if current_user.is_authenticated:
			autor = current_user.email if request.form.get("include_name") else "Anonym"
		else:
			autor = "user_not_logged_in"
		c = Chyba(
		autor = autor,
		popis = request.form.get("popis")
		)
		c.pridat_do_chyb()
		return redirect(url_for("default_views.known_bugs"))

@default_views.route("/planovane_featury")
def planovane_featury():
	return render_template("planovane_featury.html")

@default_views.route("/account", methods=["GET","POST"])
@login_required
def account():
	settings = Settings.get()
	settings.check_format()
	if request.method == "GET":
		s = Slovnik.get()
		return render_template("account.html", 
							   current_user=current_user, 
							   pocet_slovicek = len(s.slovicka), 
							   settings = settings)
	else:
		if request.form.get("zkouseni_opakovani"):
			settings.data["zkouseni_opakovani"] = not settings.data["zkouseni_opakovani"]
			settings.save()
			return redirect(url_for("default_views.account"))
		elif request.form.get("vybirani"):
			return "Not done yet" + request.form.get("uceni_choose")
		elif request.form.get("new_jazyk_button"):
			settings.add_jazyk(request.form.get("new_jazyk"))
			return redirect(url_for("default_views.account"))
