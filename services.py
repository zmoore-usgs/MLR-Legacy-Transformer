import pkg_resources
import re

from flask import request
from flask_restplus import Api, Resource, fields

from werkzeug.exceptions import BadRequest

from app import application
from flask_restplus_jwt import JWTRestplusManager, jwt_required
from utils import transform_location_to_decimal_location

# This will add the Authorize button to the swagger docs
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(application,
          title='MLR Legacy Transformer',
          description='Provides services which transform MLR legacy fields',
          default='Transformer',
          doc='/api',
          security='apiKey',
          authorizations=authorizations
          )

# Setup the Flask-JWT-Simple extension
jwt = JWTRestplusManager(api, application)

lat_lon_model = api.model('LatLonModel', {
    'latitude': fields.String,
    'longitude': fields.String,
    'coordinateDatumCode': fields.String,
})
decimal_lat_lon_model = api.model('DecimalLatLonModel', {
    'decimalLatitude': fields.Float,
    'decimalLongitude': fields.Float
})
station_name_model = api.model('StationNameModel', {
    'stationName': fields.String
})
station_ix_model = api.model('StationIxModel', {
    'stationIx': fields.String
})

expected_lat_lon_model_keys = set(iter(lat_lon_model.keys()))
expected_station_name_model_keys = set(iter(station_name_model.keys()))


def _handle_missing_keys(json_data, expected_keys):
    """
    :param dict json_data:
    :param set expected_keys:
    :raises BadRequest if any keys in expected_keys are missing from json_data
    """
    request_keys = set(iter(json_data.keys()))
    missing_keys = expected_keys.difference(request_keys)
    if missing_keys:
        raise BadRequest('Missing keys: {0}'.format(', '.join(missing_keys)))


@api.route('/transformer/decimal_location')
class DecimalLocation(Resource):

    @api.response(200, 'Successful', decimal_lat_lon_model)
    @api.response(400, 'Missing keys')
    @api.expect(lat_lon_model)
    @jwt_required
    def post(self):
        request_body = request.get_json()
        _handle_missing_keys(request_body, expected_lat_lon_model_keys)
        return transform_location_to_decimal_location(request_body.get('latitude'),
                                                      request_body.get('longitude'),
                                                      request_body.get('coordinateDatumCode'))


@api.route('/transformer/station_ix')
class StationIx(Resource):

    @api.response(200, 'Successful', station_ix_model)
    @api.response(400, "Missing keys:")
    @api.expect(station_name_model)
    @jwt_required
    def post(self):
        request_body = request.get_json()
        _handle_missing_keys(request_body, expected_station_name_model_keys)
        station_ix = re.sub('\s|[^a-zA-Z0-9]', '', request_body.get('stationName'))
        return {'stationIx': station_ix.upper()}, 200


version_model = api.model('VersionModel', {
    'version': fields.String,
    'artifact': fields.String
})


@api.route('/version')
class Version(Resource):

    @api.response(200, 'Success', version_model)
    def get(self):
        try:
            distribution = pkg_resources.get_distribution('usgs_wma_mlr_legacy_transformer')
        except pkg_resources.DistributionNotFound:
            resp = {
                "version": "local_development",
                "artifact": None
            }
        else:
            resp = {
                "version": distribution.version,
                "artifact": distribution.project_name
            }
        return resp
