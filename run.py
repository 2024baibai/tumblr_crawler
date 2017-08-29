#-*- coding=utf-8 -*-
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import *


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
