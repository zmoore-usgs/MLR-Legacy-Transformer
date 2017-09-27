
import json
from unittest import TestCase

import app

class DecimalLocationTestCase(TestCase):

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