from .extensions import ma
from .models import User, Room, Message

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True
    
    sender = ma.Nested(lambda: UserSchema())
    room = ma.Nested(lambda: RoomSchema())


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ("password_hash",)    
    
    messages = ma.List(ma.Nested(MessageSchema))


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_fk = True
    
    owner = ma.Nested(UserSchema)
    members = ma.List(ma.Nested(UserSchema))
    messages = ma.List(ma.Nested(MessageSchema))
