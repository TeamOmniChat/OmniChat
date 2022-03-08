from flask import jsonify, request
from . import room_view
from flask_login import login_required, current_user
from ..models import Room, User
from ..extensions import db
from ..schemas import RoomSchema

room_schema = RoomSchema()

@room_view.route("/new", methods=["POST"])
@login_required
def new_room():
    name = request.args.get("name")
    desc = request.args.get("desc")
    members = [current_user.id]
    members.extend(request.args.get("members", "").split(","))
    if not name or Room.query.filter_by(name=name).first() is not None:
        return jsonify({
            "status": "error",
            "message": "Invalid room name or room name already exists."
        })
    room = Room(name=name, desc=desc, owner=current_user)
    db.session.add(room)
    for member in members:
        u = User.query.get(member)
        if u is None:
            return jsonify({
                "status": "error",
                "message": "The user requested does not exist."
            })
        room.members.append(u)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Room created successfully.",
        "data": room_schema.dump(room)
    })

@room_view.route("/<id>/get")
def get_room(id):
    room = Room.query.get(id)
    if room is None:
        return jsonify({
            "status": "error",
            "message": "The room requested does not exist."
        })
    return jsonify({
        "status": "success",
        "message": "Room fetched successfully.",
        "data": room_schema.dump(room)
    })

@room_view.route("/<id>/add-members")
def add_members(id):
    room = Room.query.get(id)
    if room is None:
        return jsonify({
            "status": "error",
            "message": "The room requested does not exist."
        })
    member_ids = request.args.get("members", "").split(",")
    for member in member_ids:
        u = User.query.get(member)
        if u is None:
            return jsonify({
                "status": "error",
                "message": "The user requested does not exist."
            })
        room.members.append(u)
    db.session.add(room)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Members added successfully"
    })
