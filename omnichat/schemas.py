from .extensions import ma
from .models import User, Room

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ("password_hash",)    


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_fk = True
    
    owner = ma.Nested(UserSchema)
    members = ma.List(ma.Nested(UserSchema))
