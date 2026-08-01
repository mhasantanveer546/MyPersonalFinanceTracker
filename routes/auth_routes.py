from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import register_user, login_user_check, update_profile, change_password

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


@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile_page():
    return render_template("profile.html", user=current_user)


@auth_bp.route("/profile", methods=["POST"])
@login_required
def update_profile_route():
    username = request.form.get("username")
    email = request.form.get("email")

    result = update_profile(current_user.id, username, email)

    if result["success"]:
        return redirect(url_for("auth.profile_page"))
    else:
        return render_template("profile.html", user=current_user, error=result["message"])


@auth_bp.route("/change-password", methods=["GET"])
@login_required
def change_password_page():
    return render_template("change_password.html")


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password_route():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")

    result = change_password(current_user.id, current_password, new_password)

    if result["success"]:
        return redirect(url_for("auth.profile_page"))
    else:
        return render_template("change_password.html", error=result["message"])