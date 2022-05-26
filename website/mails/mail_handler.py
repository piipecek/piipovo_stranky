from website import mail
from flask_mail import Message
from flask import render_template, url_for



def mail_sender(mail_identifier, target, data) -> None:
    """
    Will send email, if parameters filled correctly
    """
    if mail_identifier == "reset_password":
        msg = Message("Změna hesla na 3D Portálu",
                      sender="josef.latj@gmail.com",
                      recipients=[target])
        msg.html = render_template("mails/reset_password.html", url=url_for("auth_views.reset_password", token = data, _external = True))
        mail.send(msg)

    if mail_identifier == "potvrzeni_emailu":
        msg = Message("Potvrzení e-mailu na 3D Portálu",
                      sender="josef.latj@gmail.com",
                      recipients=[target])
        msg.html = render_template("mails/potvrzeni_emailu.html", url=url_for("default_views.account_verified", token = data, _external = True))
        mail.send(msg)
    
