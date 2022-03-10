from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

room_user = db.Table("room_user",
                     db.Column("room_id", db.Integer,
                               db.ForeignKey("room.id")),
                     db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                     )


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True)
    email: str = db.Column(db.String(128), unique=True)
    password_hash: str = db.Column(db.String)
    owned_rooms = db.relationship("Room", backref="owner", lazy=True)
    messages = db.relationship("Message", backref="sender", lazy=True)

    @property
    def password(self) -> None:
        raise AttributeError('Password not readable.')

    @password.setter
    def password(self, password: str) -> None:
        # workaround for Postgres password storing
        # https://stackoverflow.com/a/38262440/13266491
        self.password_hash = generate_password_hash(password.encode("utf8")).decode("utf8")

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<User %s>' % self.username


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


class Room(db.Model):
    __tablename__ = "room"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), unique=True)
    desc: str = db.Column(db.String)
    owner_id: int = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False)
    members = db.relationship(
        "User", secondary=room_user, backref="joined_rooms")
    messages = db.relationship("Message", backref="room", lazy=True)


class Message(db.Model):
    __tablename__ = "message"

    id: int = db.Column(db.Integer, primary_key=True)
    msg: str = db.Column(db.String)
    sender_id: int = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_id: int = db.Column(db.Integer, db.ForeignKey("room.id"))
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now())
