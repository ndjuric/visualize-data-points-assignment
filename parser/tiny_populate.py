# -*- coding: utf-8 -*-
import json
from motionlogic.models.opencellid import OpenCellId


class Reader:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return True

    def read_file(self):
        with open(self.file_path) as infile:
            while True:
                lines = infile.readlines(65536)
                if not lines:
                    break
                for line in lines:
                    yield line

    def process(self):
        for line in self.read_file():
            line = line.strip()
            if not self.is_json(line):
                continue
            data = json.loads(line)
            print(data)
            ocid = OpenCellId(data)
            ocid.save()
