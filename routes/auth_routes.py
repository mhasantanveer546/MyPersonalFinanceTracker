from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required
from services.auth_service import register_user, login_user_check

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registration", methods=["GET"])
def register_page():
    return render_template("registration.html")


@auth_bp.route("/registration", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    result = register_user(username, email, password)

    if result["success"]:
        return redirect(url_for("auth.login_page"))
    else:
        return render_template("registration.html", error=result["message"])


@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    result = login_user_check(
        request.form.get("username_or_email"),
        request.form.get("password")
    )

    if result["success"]:
        login_user(result["user"])
        return redirect(url_for("dashboard.dashboard"))
    else:
        return render_template("login.html", error=result["message"])


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_page"))