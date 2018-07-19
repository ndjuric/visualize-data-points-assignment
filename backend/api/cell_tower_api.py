from flask_restful import Resource
from backend.services.cell_tower_service import CellTowerService


class CellTowerAPI(Resource):
    def get(self, bounds):
        """
        Fetch 1000 cell towers
        ---
        tags:
          - mapping
        produces:
          - application/json
        parameters:
            - name: bounds
              in: path
              description: Bounding box for which to retrieve cell tower locations
              required: true
              type: string
        responses:
            200:
                description: GeoJson Feature Collection
            500:
                description: Internal Server Error
        """
        return CellTowerService.get_cell_towers(bounds)
