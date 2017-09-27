import re

from flask import request
from flask_restplus import Api, Resource, fields

from app import application

api = Api(application,
          title='MLR Legacy Transformer',
          description='Provides services which transform MLR legacy fields',
          default='Transformer',
          doc='/api')

lat_lon_model = api.model('LatLonModel', {
    'latitude' : fields.String,
    'longitude' : fields.String,
    'coordinateDatumCode' : fields.String,
})
decimal_lat_lon_model = api.model('DecimalLatLonModel', {
    'decimalLatitude' : fields.Float,
    'decimalLongitude' : fields.Float
})
station_name_model = api.model('StationNameModel', {
    'stationName' : fields.String
})
station_ix_model = api.model('StationIxModel', {
    'stationIx' : fields.String
})

@api.route('/transformer/decimal_location')
class DecimalLocation(Resource):

    @api.response(200, 'Successful', decimal_lat_lon_model)
    @api.response(400, 'Can\'t transform location')
    @api.expect(lat_lon_model)
    def post(self):
        return 'Not yet implemented', 500


@api.route('/transformer/station_ix')
class StationIx(Resource):

    @api.response(200, 'Successful', station_ix_model)
    @api.expect(station_name_model)
    def post(self):
        try:
            station_name = request.get_json()['stationName']
        except KeyError:
            response, status = 'Missing stationName key', 400
        else:
            station_ix = re.sub('\s|[^a-zA-Z0-9]', '', station_name)
            response, status = {'stationIx' : station_ix.upper()}, 200
        return response, status