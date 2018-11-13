
import json
from unittest import TestCase, mock

import jwt

import app


@mock.patch('services.transform_location_to_decimal_location')
class DecimalLocationTestCase(TestCase):

    def setUp(self):
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None
        app.application.testing = True
        self.app_client = app.application.test_client()

    def test_good_request(self, mock):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        mock.return_value = {'decimalLatitude' : 40, 'decimalLongitude': -100}
        input = {
            'latitude': ' 400000    ',
            'longitude': ' 1000000    ',
            'coordinateDatumCode': 'NAD27      ',
        }
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(input))
        self.assertEqual(response.status_code, 200)
        expected = {
            **input,
            'decimalLatitude': 40,
            'decimalLongitude': -100,
        }
        self.assertEqual(expected, json.loads(response.data))

    def test_missing_keys(self, mock):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps({
                                            'latitudee': ' 400000    ',
                                            'longitude' : ' 1000000    ',
                                            'coordinateDatumCode' : 'NAD27      '}))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'latitude', response.data)

    def test_no_auth_header(self, mock):
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        data=json.dumps({
                                            'latitudee': ' 400000    ',
                                            'longitude': ' 1000000    ',
                                            'coordinateDatumCode': 'NAD27      '}))
        self.assertEqual(response.status_code, 401)

    def test_bad_token(self, mock):
        bad_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'bad_secret')
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                        data=json.dumps({
                                            'latitudee': ' 400000    ',
                                            'longitude': ' 1000000    ',
                                            'coordinateDatumCode': 'NAD27      '}))
        self.assertEqual(response.status_code, 422)


class StationIxTestCase(TestCase):

    def setUp(self):
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None
        app.application.testing = True
        self.app_client = app.application.test_client()

    def test_station_name_with_whitespace(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        input = {"stationName": "Station Name"}
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(input))
        self.assertEqual(response.status_code, 200)
        expected = {
            **input,
            'stationIx': 'STATIONNAME',
        }
        self.assertEqual(json.loads(response.data), expected)

    def test_station_name_with_nonalphanumerics(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        input = {"stationName": "Station#_Name1$"}
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data=json.dumps(input))
        self.assertEqual(response.status_code, 200)
        expected = {
            **input,
            'stationIx': 'STATIONNAME1',
        }
        self.assertEqual(expected, json.loads(response.data))

    def test_invalid_request_payload(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                        data='{"stationNam": "Station#_Name1$"}')
        self.assertEqual(response.status_code, 400)

    def test_no_auth_header(self):
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        data='{"stationNam": "Station#_Name1$"}')
        self.assertEqual(response.status_code, 401)

    def test_bad_token(self):
        bad_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'bad_secret')
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                        data='{"stationName": "Station#_Name1$"}')
        self.assertEqual(response.status_code, 422)

