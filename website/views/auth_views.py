from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from website import db
from website.helpers.check_files import check_files_or_create
from website.helpers.check_updated_slovnik import check_if_slovnik_updated_or_update
from website.helpers.check_updated_historie import check_if_historie_updated_or_update

auth_views = Blueprint("auth_views",__name__, template_folder="auth")

@auth_views.route("/login", methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		user = User.query.filter_by(email=email).first()
		if user and check_password_hash(user.password, password):
			login_user(user, remember=True)
			flash("úspěšné přihlášení", category="info")
			check_files_or_create()
			check_if_slovnik_updated_or_update()
			check_if_historie_updated_or_update()
			return redirect(url_for("default_views.dashboard"))
		else:
			flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))

@auth_views.route("/register", methods=["GET","POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")

		user = User.query.filter_by(email=email).first()
		if user:
			flash("Tento email je už zaregistrovaný. Použij prosím jiný", category="error")
			return redirect(url_for("auth_views.register"))
		else:
			new_user = User(email=email, password=generate_password_hash(password, method="sha256"))
			db.session.add(new_user)
			db.session.commit()
			flash("Úspěšně zaregistrováno. Teď se přihlaš :P", category="info")
			return redirect(url_for("auth_views.login"))

@auth_views.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have been odhlášen.", category="info")
	return redirect(url_for("default_views.home"))






