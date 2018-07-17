from motionlogic.models.opencellid import OpenCellId


class CellTowerService:
    @staticmethod
    def get_cell_towers(bounds):
        return OpenCellId.get_cell_towers(bounds)

    @staticmethod
    def get_png(bounds):
        return OpenCellId.get_png(bounds)
