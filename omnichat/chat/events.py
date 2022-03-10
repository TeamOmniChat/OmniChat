
from flask import session
from flask_login import current_user
from flask_socketio import join_room, leave_room, rooms
from ..extensions import socketio, db
from ..schemas import UserSchema
from ..models import Message, User, Room

user_schema = UserSchema()

def add_current_user_to_room(roomname):
    join_room(roomname)
    session["room"] = roomname
    return {
        "status": "success",
        "message": "User joined to room successfully."
    }

@socketio.on("chat")
def handle_chat(msg):
    evt = msg["event"] if "event" in msg else "users"
    user = msg["user"]
    room = msg["room"]
    if user["username"] != current_user.username:
        return
    match evt:
        case "join":
            if room["name"] in rooms(): return
            join_room(room["name"])
            socketio.emit("system", {
                "type": "join",
                "message": f"Welcome {user['username']} to {room['name']} !"
            }, room=room["name"])
        case "text":
            message = Message(msg=msg["msg"], sender=User.query.filter_by(username=user["username"]), room=Room.query.filter_by(name=room["name"]))
            db.session.add(message)
            db.session.commit()
            socketio.emit("message", {
                "type": "message",
                "message": msg["msg"],
                "user": user,
                "room": room
            }, room=room["name"])
        case "leave":
            leave_room(room)
            socketio.emit("system", {
                "type": "leave",
                "message": f"User {user['username']} has left the room."
            }, room=room["name"])
        # TODO add more events
