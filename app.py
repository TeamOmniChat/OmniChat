from omnichat import create_app
from omnichat.models import *
from omnichat.extensions import socketio

app = create_app()

def deploy():
    from omnichat import db
    from flask_migrate import upgrade, migrate, init, stamp

    with app.app_context():
        db.create_all()
        init()
        stamp()
        migrate()
        upgrade()

@app.shell_context_processor
def shell_context_processor():
    return dict(deploy=deploy, db=db, User=User)

if __name__ == '__main__':
    socketio.run(app)
