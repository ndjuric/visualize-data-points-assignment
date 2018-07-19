import os
from parser import Reader
from flask_script import Manager
from flask_migrate import MigrateCommand

from motionlogic import create_app
from motionlogic.models.opencellid import OpenCellId

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def parse_mccs(mccs):
    tmp_codes = []
    if mccs is not '':
        tmp_codes = mccs.split(',')
    mcc_list = [x for x in tmp_codes if x.isdigit()]
    mcc_list = list(set(mcc_list))
    if not mcc_list:
        mcc_list.append('602')
    return mcc_list


@manager.command
def parse(mccs=''):
    mcc_list = parse_mccs(mccs)

    csv_file = os.path.join(os.path.abspath('.'), 'data', 'cell_towers.csv')
    reader = Reader(csv_file, mcc_list)
    reader.parse()


@manager.command
def geojson():
    points_file = os.path.join(os.path.abspath('.'), 'data', 'points.json')
    with open(points_file, 'a') as points_fh:
        for geom in OpenCellId.get_geojson():
            points_fh.write(geom)


if __name__ == '__main__':
    manager.run()
