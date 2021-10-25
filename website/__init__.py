from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "r Schornstein"
	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

	db.init_app(app)

	def check_if_database_exists_else_create(app):
		if not os.path.exists("website/" + DB_NAME):
			db.create_all(app=app)
			print("created_db")

	from .views.default_views import default_views
	from .views.auth_views import auth_views
	from .views.slovnik_views import slovnik_views
	from .views.visuals_views import visuals_views

	app.register_blueprint(default_views, url_prefix="/")
	app.register_blueprint(auth_views, url_prefix="/auth")
	app.register_blueprint(slovnik_views, url_prefix="/slovnik")
	app.register_blueprint(visuals_views, url_prefix="/visuals")

	from .models.user import User

	check_if_database_exists_else_create(app)

	login_manager = LoginManager()
	login_manager.login_view = "auth_views.login"
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))  # get rovou kouka na primary key, nemusim delat filter_by(id=id)


	return app