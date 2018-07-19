import json
import pandas as pd
from motionlogic.models.opencellid import OpenCellId


class Reader:
    def __init__(self, file_path, mcc_list=None):
        self.file_path = file_path
        self.mcc_list = mcc_list
        if self.mcc_list is None:
            self.mcc_list = []

    def parse(self):
        print('Trying to parse %s' % self.file_path)
        try:
            csv_data = pd.read_csv(self.file_path)
        except Exception as e:
            print('Error reading %s: %s' % (self.file_path, e.message))
            return

        if not self.mcc_list:
            parse_data = csv_data
        else:
            parse_data = csv_data[csv_data['mcc'].isin(self.mcc_list)]
            parse_data.reset_index(inplace=True, drop=True)

        for idx, row in parse_data.iterrows():
            line = row.to_dict()
            try:
                print(json.dumps(line))
                open_cell_id = OpenCellId(line)
                open_cell_id.save()
            except Exception as e:
                print(e)
                print('in line:', idx)
                pass

        print('Done!')
