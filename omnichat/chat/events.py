
from flask_socketio import emit, join_room, leave_room
from ..extensions import socketio
from ..schemas import UserSchema
from ..models import User

user_schema = UserSchema()

def add_current_user_to_room(roomname):
    join_room(roomname)
    return {
        "status": "success",
        "message": "User joined to room successfully."
    }

@socketio.on("chat")
def handle_chat(msg):
    evt = msg["event"] if "event" in msg else "users"
    match evt:
        case "join":
            user = msg["user"]
            room = msg["room"]
            add_current_user_to_room(room["name"])
            socketio.emit("chat", {
                "type": "newuser",
                "message": f"Welcome {user['username']} to {room['name']} !"
            }, room=room["name"])
        # TODO add more events
