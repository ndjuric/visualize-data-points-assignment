from backend.models.opencellid import OpenCellId


class CellTowerService:
    @staticmethod
    def get_cell_towers(bounds):
        return OpenCellId.get_cell_towers(bounds)
