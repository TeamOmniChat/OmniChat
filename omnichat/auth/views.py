from flask import jsonify, request, session
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from ..models import User
from ..extensions import db, login_manager
from ..schemas import UserSchema

user_schema = UserSchema()


@auth.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    if User.query.filter_by(username=username).first() is not None \
            or User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "error": "Invalid payload",
            "detail": "Username or email already taken."
        }), 400
    password = request.json.get("password")
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": f"User {username} registered successfully."
    })


@auth.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({
            "error": "Already authenticated",
            "detail": "You already logged in."
        }), 403
    username: str = request.json.get("username")
    password: str = request.json.get("password")
    user: User = User.query.filter_by(username=username).first()
    if user.verify_password(password):
        login_user(user, True)
        session["user"] = user_schema.dump(user)
        return jsonify({
            "message": f"Logged in as {user.username}."
        })
    return jsonify({
        "error": "Invalid payload",
        "detail": "Unable to log into your account. Please check if your username and password are correct."
    }), 400


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({
        "message": "Logged out successfully."
    })


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": "Unauthenticated",
        "detail": "You're not logged in."
    }), 401


@auth.route("/current_user")
@login_required
def get_current_user():
    return jsonify({
        "data": user_schema.dump(current_user)
    })
