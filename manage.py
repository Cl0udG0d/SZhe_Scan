from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from init import app
from app.model.models import *


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
