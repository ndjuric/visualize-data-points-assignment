from flask_restful import Resource
from motionlogic.services.cell_tower_service import CellTowerService


class TilePngAPI(Resource):
    def get(self, bounds):
        """
        Generate png for provided bounds
        ---
        tags:
          - mapping
        produces:
          - application/json
        parameters:
            - name: bounds
              in: path
              description: Bounding box for which to generate png
              required: true
              type: string
        responses:
            200:
                description: GeoJson Feature Collection
            500:
                description: Internal Server Error
        """
        return CellTowerService.get_png(bounds)
