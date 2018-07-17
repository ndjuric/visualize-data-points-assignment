import os
from parser import Reader
from flask_script import Manager
from flask_migrate import MigrateCommand

from motionlogic import create_app

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def loadstuff():
    csv_file = os.path.join(os.path.abspath('.'), 'data', 'egypt.json')
    reader = Reader(csv_file)
    reader.process()


if __name__ == '__main__':
    manager.run()
