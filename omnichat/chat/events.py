
import functools

from flask import request, session
from flask_jwt_extended import (current_user, decode_token, jwt_required,
                                verify_jwt_in_request)
from flask_socketio import disconnect, emit, join_room, leave_room, rooms

from ..extensions import db, socketio
from ..models import Message, Room, User
from ..schemas import UserSchema


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(msg):
        if not msg.get("token", None):
            disconnect()
        else:
            u = User.query.get(decode_token(msg["token"])["sub"])
            if u is None:
                disconnect()
            else:
                return f(msg, u)
    return wrapped


user_schema = UserSchema(exclude=("messages",))


def add_current_user_to_room(roomname):
    join_room(roomname)
    session["room"] = roomname  # set session for current room
    return {
        "status": "success",
        "message": "User joined to room successfully."
    }


@socketio.on("join")
@authenticated_only
def handle_join(msg, sender):
    room = msg["room"]
    if room["name"] in rooms():
        return
    join_room(room["name"])
    socketio.emit("system", {
        "type": "join",
        "message": f"Welcome {sender.username} to {room['name']} !"
    }, room=room["name"])


@socketio.on("text")
@authenticated_only
def handle_text(msg, sender):
    room = msg["room"]
    message = Message(msg=msg["msg"], sender=User.query.filter_by(
        username=sender.username).first(), room=Room.query.filter_by(name=room["name"]).first())
    db.session.add(message)
    db.session.commit()
    socketio.emit("message", {
        "type": "text",
        "message": msg["msg"],
        "user": user_schema.dump(sender),
        "room": room
    }, room=room["name"])


@socketio.on("leave")
@authenticated_only
def handle_leave(msg, sender):
    room = msg["room"]
    leave_room(room["name"])
    socketio.emit("system", {
        "type": "leave",
        "message": f"User {sender.username} has left the room."
    }, room=room["name"])
