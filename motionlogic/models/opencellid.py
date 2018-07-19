from motionlogic import db
from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction
import json


class ST_Point(GenericFunction):
    """ Exposes PostGIS ST_SetSRID function """
    name = 'ST_Point'
    type = Geometry


class ST_MakeEnvelope(GenericFunction):
    """ Exposes PostGIS ST_MakeEnvelope function """
    name = 'ST_MakeEnvelope'
    type = Geometry


class ST_AsPNG(GenericFunction):
    """ Exposes PostGIS ST_AsPNG function """
    name = 'ST_AsPNG'
    type = Geometry


class ST_AsGeoJSON(GenericFunction):
    """ Exposes PostGIS ST_AsGeoJSON function """
    name = 'ST_AsGeoJSON'
    type = Geometry


class ST_Transform(GenericFunction):
    """ Exposes PostGIS ST_Transform function """
    name = 'ST_Transform'
    type = Geometry


class ST_AsText(GenericFunction):
    """ Exposes PostGIS ST_AsText function """
    name = 'ST_AsText'
    type = Geometry


class OpenCellId(db.Model):
    """ Describes an individual mapping feature """
    __tablename__ = "open_cell_id"

    id = db.Column(db.Integer, primary_key=True)
    mcc = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)

    radio = db.Column(db.String, nullable=False)
    cell = db.Column(db.Integer, nullable=False)
    net = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, nullable=True)

    lon = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    range = db.Column(db.Integer, nullable=False)
    averageSignal = db.Column(db.Integer, nullable=False)
    samples = db.Column(db.Integer, nullable=False)
    changeable = db.Column(db.Integer, nullable=False)

    created = db.Column(db.Integer, nullable=False)
    updated = db.Column(db.Integer, nullable=False)

    coord = db.Column(Geometry('POINT'), nullable=True)

    def __init__(self, val_dict):
        for key, value in val_dict.items():
            setattr(self, key, value)
        val_dict_keys = val_dict.keys()
        if ('lat' in val_dict_keys) and ('lon' in val_dict_keys):
            self.coord = ST_Point(self.lon, self.lat)

    @staticmethod
    def get_cell_towers(bounds):
        bb = bounds.split(',')
        if len(bb) is not 4:
            return json.dumps([])

        cell_towers = db.session.query(OpenCellId).filter(
            OpenCellId.coord.intersects(ST_MakeEnvelope(*bb))
        ).limit(5000)

        output = []
        for data in cell_towers:
            output.append(
                {
                    'id': data.id,
                    'mcc': data.mcc,
                    'radio': data.radio,
                    'range': data.range,
                    'lon': data.lon,
                    'lat': data.lat
                }
            )
        return json.dumps(output)

    @staticmethod
    def get_geojson():
        sql = 'SELECT ST_AsGeoJSON(open_cell_id.coord) AS "ST_AsGeoJSON_1" FROM open_cell_id'
        result = db.engine.execute(sql)
        for r in result:
            for x in r:
                yield x

    def save(self):
        db.session.add(self)
        db.session.commit()
