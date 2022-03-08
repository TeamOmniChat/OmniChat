import os
from flask import Flask
from .extensions import db, migrate, login_manager, bcrypt, ma, socketio

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    socketio.init_app(app)

    from .auth import auth as auth_bp
    from .room import room_view as room_bp
    from .chat import chat as chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(chat_bp)

    return app
