from models.user import User
from models import db
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(username, email, password):
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return {"success": False, "message": "Username or email already exists."}

    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    return {"success": True, "message": "User registered successfully.", "user": new_user}


def login_user_check(username_or_email, password):
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and check_password_hash(user.password_hash, password):
        return {"success": True, "message": "Login successful.", "user": user}

    return {"success": False, "message": "Invalid username/email or password."}


def update_profile(user_id, username, email):
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "message": "User not found."}

    existing = User.query.filter(
        User.id != user_id,
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        return {"success": False, "message": "Username or email already taken by another user."}

    user.username = username
    user.email = email
    db.session.commit()

    return {"success": True, "message": "Profile updated successfully.", "user": user}


def change_password(user_id, current_password, new_password):
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "message": "User not found."}

    if not check_password_hash(user.password_hash, current_password):
        return {"success": False, "message": "Current password is incorrect."}

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return {"success": True, "message": "Password changed successfully."}