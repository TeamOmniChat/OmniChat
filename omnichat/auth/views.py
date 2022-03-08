from flask import jsonify, request, session
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from ..models import User
from ..extensions import db, login_manager
from ..schemas import UserSchema

user_schema = UserSchema()

@auth.route("/register", methods=["POST"])
def register():
    username = request.args.get("username")
    email = request.args.get("email")
    if User.query.filter_by(username=username).first() is not None \
        or User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "status": "error",
            "message": "Username or email already taken."
        })
    password = request.args.get("password")
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "status": "success",
        "username": username
    })

@auth.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({
            "status": "error",
            "message": "You already logged in."
        })
    username: str = request.args.get("username")
    password: str = request.args.get("password")
    user: User = User.query.filter_by(username=username).first()
    if user.verify_password(password):
        login_user(user, True)
        session["user"] = user_schema.dump(user)
        return jsonify({
            "status": "success",
            "message": f"Logged in as {user.username}."
        })
    return jsonify({
        "status": "error",
        "message": "Unable to log into your account. Please check if your username and password are correct."
    })

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully."
    })

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "status": "error",
        "message": "You're not logged in."
    })

@auth.route("/current_user")
@login_required
def get_current_user():
    return jsonify({
        "status": "success",
        "data": user_schema.dump(current_user)
    })
