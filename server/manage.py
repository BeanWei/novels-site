import os

from app import create_app, db
from app.models import User, Role, Novel
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Novel=Novel)

'''
数据库迁移指令
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
'''
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    '''
    部署命令
    '''
    from flask_migrate import upgrade
    upgrade()

if __name__ == "__main__":
    manager.run()