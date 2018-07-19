import json
from backend.models.opencellid import OpenCellId


class CellTowerService:
    @staticmethod
    def get_cell_towers(bounds):
        bbox = bounds.split(',')
        if len(bbox) is not 4:
            return json.dumps([])
        return OpenCellId.get_cell_towers(bbox)
