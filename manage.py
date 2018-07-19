import os
from parser import OpenCellIdParser
from flask_script import Manager
from flask_migrate import MigrateCommand

from backend import create_app
from backend.models.opencellid import OpenCellId

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
    parser = OpenCellIdParser(csv_file, mcc_list)
    parser.run()


@manager.command
def geojson(mccs=''):
    mcc_list = parse_mccs(mccs)

    files = []
    for mcc in mcc_list:
        points_file = os.path.join(os.path.abspath('.'), 'data', mcc + '.json')
        files.append(points_file)
        with open(points_file, 'a') as points_fh:
            for geom in OpenCellId.get_geojson_points_for_mcc(mcc):
                points_fh.write(geom)

    for file in files:
        if os.stat(file).st_size == 0:
            os.remove(file)


if __name__ == '__main__':
    manager.run()
