from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user


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
	return "not implemented yet"

@default_views.route("/nahlasit_bug")
@login_required
def nahlasit_bug():
	return "not implemented yet"
