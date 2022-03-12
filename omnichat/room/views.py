from flask import jsonify, request
from . import room_view
from flask_jwt_extended import jwt_required, current_user
from ..models import Room, User
from ..extensions import db
from ..schemas import RoomSchema

room_schema = RoomSchema()

@room_view.route("/", methods=["POST"])
@jwt_required()
def new_room():
    name = request.json.get("name")
    desc = request.json.get("desc")
    members = [current_user.id]
    members.extend(request.json.get("members", []))
    if not name or Room.query.filter_by(name=name).first() is not None:
        return jsonify({
            "error": "Invalid payload",
            "detail": "Invalid room name or room name already exists."
        }), 400
    room = Room(name=name, desc=desc, owner=current_user)
    db.session.add(room)
    for member in members:
        u = User.query.get(member)
        if u is None:
            return jsonify({
                "error": "Invalid payload",
                "detail": "The user requested does not exist."
            }), 400
        room.members.append(u)
    db.session.commit()
    return jsonify({
        "message": "Room created successfully.",
        "data": room_schema.dump(room)
    })

@room_view.route("/<id>")
def get_room(id):
    room = Room.query.get(id)
    if room is None:
        return jsonify({
            "error": "Invalid payload",
            "detail": "The room requested does not exist."
        }), 400
    return jsonify({
        "message": "Room fetched successfully.",
        "data": room_schema.dump(room)
    })

@room_view.route("/<id>/add-members", methods=["POST"])
@jwt_required()
def add_members(id):
    room = Room.query.get(id)
    if room is None:
        return jsonify({
            "error": "Invalid payload",
            "detail": "The room requested does not exist."
        }), 400
    if room.owner_id != current_user.id:
        return jsonify({
            "error": "Forbidden",
            "detail": "Current user does not match the room owner."
        }), 403
    member_ids = request.json.get("members", [])
    for member in member_ids:
        u = User.query.get(member)
        if u is None:
            return jsonify({
                "error": "Invalid payload",
                "detail": "The user requested does not exist."
            }), 400
        if u in room.members: continue
        room.members.append(u)
    db.session.add(room)
    db.session.commit()
    return jsonify({
        "message": "Members added successfully"
    })
