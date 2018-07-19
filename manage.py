import os
import subprocess
from parser import OpenCellIdParser
from flask_script import Manager
from flask_migrate import MigrateCommand

from backend import create_app
from backend.models.opencellid import OpenCellId

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def parse_mccs_param(mccs):
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
    mcc_list = parse_mccs_param(mccs)

    csv_file = os.path.join(os.path.abspath('.'), 'data', 'cell_towers.csv')
    parser = OpenCellIdParser(csv_file, mcc_list)
    parser.run()


@manager.command
def geojson(mccs=''):
    mcc_list = parse_mccs_param(mccs)

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


@manager.command
def mbtiles(mccs=''):
    mcc_list = parse_mccs_param(mccs)

    for mcc in mcc_list:
        points_file = os.path.join(os.path.abspath('.'), 'data', mcc + '.json')
        if not os.path.exists(points_file):
            print('%s does not exist!' % points_file)
            continue
        print('do stuff with %s' % points_file)
        # docker-compose run tippecanoe sh -c 'tippecanoe -o /data/out.mbtiles -zg --drop-densest-as-needed /data/602.json'
        tippecanoe_base_command = 'tippecanoe -o /data/{0}.mbtiles -zg --drop-densest-as-needed /data/{0}.json'
        tippecanoe_command = tippecanoe_base_command.format(mcc)
        subprocess.call(["docker-compose", "run", "tippecanoe", "sh", "-c", tippecanoe_command])




if __name__ == '__main__':
    manager.run()
