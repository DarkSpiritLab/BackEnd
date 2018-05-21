import os
from app import create_app, db, socketio
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from flask_socketio import emit


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    socketio.run(app, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()


