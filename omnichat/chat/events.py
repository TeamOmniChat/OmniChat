
import functools

from flask import request, session
from flask_login import current_user
from flask_socketio import disconnect, emit, join_room, leave_room, rooms

from ..extensions import db, socketio
from ..models import Message, Room, User
from ..schemas import UserSchema


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


user_schema = UserSchema()


def add_current_user_to_room(roomname):
    join_room(roomname)
    session["room"] = roomname  # set session for current room
    return {
        "status": "success",
        "message": "User joined to room successfully."
    }


@socketio.on("join")
@authenticated_only
def handle_join(msg):
    user = msg["user"]
    room = msg["room"]
    # check if current user is the currently logged in user
    # can't use this in Postman since cookies between Socket requests
    # and normal HTTP requests don't sync
    # so remember to comment it out when testing APIs with Postman
    # however, in production, you MUST uncomment this to prevent
    # hackers use this issue to fake messages
    if user["username"] != current_user.username:
        return
    if room["name"] in rooms():
        return
    join_room(room["name"])
    socketio.emit("system", {
        "type": "join",
        "message": f"Welcome {user['username']} to {room['name']} !"
    }, room=room["name"])


@socketio.on("text")
@authenticated_only
def handle_text(msg):
    user = msg["user"]
    room = msg["room"]
    if user["username"] != current_user.username:
        return
    message = Message(msg=msg["msg"], sender=User.query.filter_by(
        username=user["username"]).first(), room=Room.query.filter_by(name=room["name"]).first())
    db.session.add(message)
    db.session.commit()
    socketio.emit("message", {
        "type": "message",
        "message": msg["msg"],
        "user": user,
        "room": room
    }, room=room["name"])


@socketio.on("leave")
@authenticated_only
def handle_leave(msg):
    user = msg["user"]
    room = msg["room"]
    if user["username"] != current_user.username:
        return
    leave_room(room["name"])
    socketio.emit("system", {
        "type": "leave",
        "message": f"User {user['username']} has left the room."
    }, room=room["name"])
