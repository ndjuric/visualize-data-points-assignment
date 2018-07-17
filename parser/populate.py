# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
from motionlogic.models.opencellid import OpenCellId


def populate(csv_file, mcc_list):
    print('Populating OpenCellId ..')
    try:
        csv_data = pd.read_csv(csv_file)
    except Exception as e:
        print('Error reading OpenCellId data')
        print(e.message)
        return

    good_data = csv_data[csv_data['mcc'].isin(mcc_list)]
    good_data.reset_index(inplace=True, drop=True)

    for idx, row in good_data.iterrows():
        line = row.to_dict()
        try:
            print(json.dumps(line))
            # ocid = OpenCellId(line)
            # ocid.save()
        except Exception as e:
            print(e)
            print('in line:', idx)
            pass

    print('Done!')


def main():
    csv_file = os.path.join(os.path.abspath('.'), 'data', 'cell_towers.csv')
    required_mcc_list = [602, ]  # egypt should be 602?
    populate(csv_file, required_mcc_list)


if __name__ == '__main__':
    main()
