from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_login import LoginManager
from flask_mail import Mail
from .helpers.check_files import check_files_or_create

db = SQLAlchemy()
DB_NAME = "database.db"
cors = CORS()
mail = Mail()



def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "r Schornstein"
	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
	app.config["MAIL_SERVER"] = "smtp.googlemail.com"
	app.config["MAIL_PORT"] = "587"
	app.config["MAIL_USE_TLS"] = True
	app.config["MAIL_USERNAME"] = "josef.latj@gmail.com"
	app.config["MAIL_PASSWORD"] = "gewfrzvyateqfoya"

	db.init_app(app)
	cors.init_app(app)
	mail.init_app(app)

	def check_if_database_exists_else_create(app):
		if not os.path.exists("website/" + DB_NAME):
			db.create_all(app=app)
			print("created_db")

	from .views.default_views import default_views
	from .views.auth_views import auth_views
	from .views.slovnik_views import slovnik_views
	from .views.visuals_views import visuals_views
	from .views.richard_views import richard_views

	app.register_blueprint(default_views, url_prefix="/")
	app.register_blueprint(auth_views, url_prefix="/auth")
	app.register_blueprint(slovnik_views, url_prefix="/slovnik")
	app.register_blueprint(visuals_views, url_prefix="/visuals")
	app.register_blueprint(richard_views, url_prefix="/api")

	from .models.user import User

	check_if_database_exists_else_create(app)
	check_files_or_create()

	login_manager = LoginManager()
	login_manager.login_view = "auth_views.login"
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))  # get rovou kouka na primary key, nemusim delat filter_by(id=id)

	@app.errorhandler(404)
	def not_found(e):
		return render_template("not_found.html"), 404

	return app