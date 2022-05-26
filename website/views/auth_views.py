from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from website import db
from website.mails.mail_handler import mail_sender
from website.helpers.create_user_files import create_user_files

auth_views = Blueprint("auth_views",__name__, template_folder="auth")

@auth_views.route("/login", methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("default_views.dashboard"))
	if request.method == "GET":
		return render_template("auth_login.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě přiliš dlouhý.", category="error")
			return redirect(url_for("auth_views.login"))
		if len(password) > 300:    
			flash("Zadané heslo bylo určitě příliš dlouhé.", category="error")
			return redirect(url_for("auth_views.login"))
		user = User.query.filter_by(email=email).first()
		if user and check_password_hash(user.password, password):
			login_user(user, remember=True)
			flash("úspěšné přihlášení", category="success")
			return redirect(url_for("default_views.dashboard"))
		else:
			flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))

@auth_views.route("/register", methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("default_views.dashboard"))
	if request.method == "GET":
		return render_template("auth_register.html")
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
			login_user(new_user, remember=True)
			create_user_files()
			return redirect(url_for("default_views.dashboard"))

@auth_views.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have been odhlášen.", category="info")
	return redirect(url_for("default_views.dashboard"))


@auth_views.route("/reset_password", methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("default_views.home"))
	if request.method == "GET":
		return render_template("auth_request_reset.html")
	else:
		email = request.form.get("email")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě moc dlouhý.", category="error")
			return redirect(url_for("auth_views.request_reset"))
		user = User.query.filter_by(email=email).first()
		if user:
			mail_sender(mail_identifier="reset_password", target=email, data=user.get_reset_token())
		flash("Pokud existuje uživatel s tímto e-mailem, byl mu odeslán ověřovací e-mail.", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("default_views.home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
		return redirect(url_for("auth_views.request_reset"))
	if request.method == "GET":
		return render_template("auth_reset_password.html")
	else:
		user.password = generate_password_hash(request.form.get("password"), method="sha256")
		db.session.commit()
		flash("Heslo změněno, můžete se nyní přihlásit:", category="info")
		return redirect(url_for("auth_views.login"))



