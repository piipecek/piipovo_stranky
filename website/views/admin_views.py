from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.json_handlers.admin_handling import is_admin
from website.models.chyba import Chyba
from website.models.user import User
from website.json_handlers.logs_handling import delete_logs
import json
import shutil
from website.paths.paths import user_data_folder_path


admin_views = Blueprint("admin_views",__name__)


# @admin_views.route("/", methods=["GET","POST"])
# def ():
#     if current_user.is_authenticated:
#         if is_admin(current_user.email):
#             if request.method == "GET":
#                 return render_template(".html")
#             else:
#                 return None
    
#     flash("Na tuto stránku nemáte přístup.", "error")
#     return redirect(url_for("default_views.home"))

@admin_views.route("/")
@admin_views.route("/dashboard")
def admin_dashboard():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            flash("Zkouška error hlášky", category="error")
            flash("Zkouška success hlášky", category="success")
            flash("Zkouška info hlášky", category="info")
            return render_template("admin_dashboard.html", pocet_bugu = Chyba.pocet_neresenych())
    
    flash("Na tuto stránku nemáte přístup.", "error")
    return redirect(url_for("default_views.home"))


@admin_views.route("/uprava_znamych_bugu", methods=["GET","POST"])
def uprava_znamych_bugu():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            if request.method == "GET":
                return render_template("admin_uprava_znamych_chyb.html")
            else:
                Chyba.save_po_upravach(json.loads(request.form.get("result")))
                return redirect(url_for("admin_views.admin_dashboard"))
    
    flash("Na tuto stránku nemáte přístup.", "error")
    return redirect(url_for("default_views.home"))
    

@admin_views.route("/logs_file", methods=["GET","POST"])
def logs_file():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            if request.method == "GET":
                return render_template("admin_logs_file.html")
            else:
                delete_logs()
                return redirect(url_for("admin_views.admin_dashboard"))

    flash("Na tuto stránku nemáte přístup.", "error")
    return redirect(url_for("default_views.home"))


@admin_views.route("/edit_users", methods=["GET","POST"])
def edit_users():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            if request.method == "GET":
                return render_template("admin_edit_users.html")
            else:
                result = request.form.get("result")
                folder_to_delete = user_data_folder_path() / result
                shutil.rmtree(folder_to_delete)
                User.query.get(int(result)).odstranit()
                flash("User smazán", category="success")
                return redirect(url_for("admin_views.admin_dashboard"))
    
    flash("Na tuto stránku nemáte přístup.", "error")
    return redirect(url_for("default_views.home"))