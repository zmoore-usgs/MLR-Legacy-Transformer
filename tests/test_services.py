
import json
from unittest import TestCase, mock

import app

@mock.patch('services.transform_location_to_decimal_location')
class DecimalLocationTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()

    def test_good_request(self, mock):
        mock.return_value = {'decimalLatitude' : 40, 'decimalLongitude': -100}
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        data=json.dumps({
                                            'latitude': ' 400000    ',
                                            'longitude' : ' 1000000    ',
                                            'coordinateDatumCode' : 'NAD27      '}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'decimalLatitude' : 40, 'decimalLongitude': -100})

    def test_missing_keys(self, mock):
        response = self.app_client.post('/transformer/decimal_location',
                                        content_type='application/json',
                                        data=json.dumps({
                                            'latitudee': ' 400000    ',
                                            'longitude' : ' 1000000    ',
                                            'coordinateDatumCode' : 'NAD27      '}))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'latitude', response.data)


class StationIxTestCase(TestCase):

    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()

    def test_station_name_with_whitespace(self):
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        data='{"stationName": "Station Name"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'stationIx': 'STATIONNAME'})

    def test_station_name_with_nonalphanumerics(self):
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        data='{"stationName": "Station#_Name1$"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'stationIx': 'STATIONNAME1'})

    def test_invalid_request_payload(self):
        response = self.app_client.post('/transformer/station_ix',
                                        content_type='application/json',
                                        data='{"stationNam": "Station#_Name1$"}')
        self.assertEqual(response.status_code, 400)


