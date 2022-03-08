from flask import Blueprint

chat = Blueprint("chat", __name__, url_prefix="/")

from . import events
