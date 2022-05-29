from flask_login import UserMixin
from website import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password =db.Column(db.String(256))

	def get_reset_token(self, expires_sec = 9000) -> str:
		s = Serializer(current_app.config["SECRET_KEY"],  expires_sec)
		return s.dumps({"user_id": self.id}).decode("utf-8") 

	@staticmethod
	def verify_reset_token(token) -> "User":
		s = Serializer(current_app.config["SECRET_KEY"])
		try:
			user_id = s.loads(token)["user_id"]
		except:
			return None
		return User.query.get(user_id)

	def get_basic_info(self) -> dict:
		return {
			"id": self.id,
			"email":self.email,
		}

	def odstranit(self):
		db.session.delete(self)
		db.session.commit()