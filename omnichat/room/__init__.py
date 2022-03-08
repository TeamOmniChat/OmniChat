from flask import Blueprint

room_view = Blueprint('room', __name__, url_prefix='/room')

from . import views
