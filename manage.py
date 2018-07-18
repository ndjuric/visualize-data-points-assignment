import os
from parser import Reader
from flask_script import Manager
from flask_migrate import MigrateCommand

from motionlogic import create_app
from motionlogic.models.opencellid import OpenCellId

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def loadstuff():
    csv_file = os.path.join(os.path.abspath('.'), 'data', 'egypt.json')
    reader = Reader(csv_file)
    reader.process()


@manager.command
def geojson():
    points_file = os.path.join(os.path.abspath('.'), 'data', 'points.json')
    with open(points_file, 'a') as points_fh:
        for geom in OpenCellId.get_geojson():
            points_fh.write(geom)


if __name__ == '__main__':
    manager.run()
