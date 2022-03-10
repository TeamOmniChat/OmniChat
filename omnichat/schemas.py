from .extensions import ma
from .models import User, Room, Message

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True
    
    sender = ma.Nested(lambda: UserSchema(exclude=("messages",)))
    room = ma.Nested(lambda: RoomSchema(exclude=("messages",)))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ("password_hash",)    
    
    messages = ma.List(ma.Nested(MessageSchema(exclude=("sender",))))


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_fk = True
    
    owner = ma.Nested(UserSchema(exclude=("messages",)))
    members = ma.List(ma.Nested(UserSchema(exclude=("messages",))))
    messages = ma.List(ma.Nested(MessageSchema(exclude=("room",))))
