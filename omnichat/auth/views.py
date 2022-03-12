from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, current_user, create_access_token
from datetime import timedelta

from . import auth
from ..models import User
from ..extensions import db, jwt
from ..schemas import UserSchema

user_schema = UserSchema(exclude=("messages",))


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
    username: str = request.json.get("username")
    password: str = request.json.get("password")
    user: User = User.query.filter_by(username=username).first()
    if user.verify_password(password):
        access_token = create_access_token(user, expires_delta=timedelta(days=15))
        session["user"] = user_schema.dump(user)
        return jsonify({
            "token": access_token
        })
    return jsonify({
        "error": "Invalid payload",
        "detail": "Unable to log into your account. Please check if your username and password are correct."
    }), 400


@jwt.unauthorized_loader
def unauthorized(why):
    return jsonify({
        "error": "Unauthenticated",
        "detail": why
    }), 401


@jwt.token_verification_failed_loader
def verification_failed(header, payload):
    return jsonify({
        "error": "Token verify failed.",
        "detail": {
            "header": header,
            "payload": payload
        }
    }), 401


@auth.route("/who-am-i")
@jwt_required()
def who_am_i():
    return jsonify({
        "data": user_schema.dump(current_user)
    })
