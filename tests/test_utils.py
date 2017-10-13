
from unittest import TestCase

from utils import transform_to_decimal_degrees, transform_latitude_to_decimal_degrees, \
    transform_longitude_to_decimal_degrees, transform_location_to_decimal_location

class TestTransformToDecimalDegrees(TestCase):

    def test_zero_values(self):
        self.assertEqual(transform_to_decimal_degrees('00', '00', '00.0'), 0)
        self.assertEqual(transform_to_decimal_degrees('-000', '00', '00'), 0)

    def test_without_decimal_seconds(self):
        self.assertAlmostEqual(transform_to_decimal_degrees(' 97', '43', '12'), 97.72, 2)
        self.assertAlmostEqual(transform_to_decimal_degrees('-123', '43', '49'), -123.73027778, 8)

    def test_with_decimal_seconds(self):
        self.assertAlmostEqual(transform_to_decimal_degrees(' 97', '43', '12.56'), 97.72015556, 8)
        self.assertAlmostEqual(transform_to_decimal_degrees('-123', '43', '49.231'), -123.730341, 5)


class TestTransformLatitudeToDecimalDegrees(TestCase):

    def test_zero_values(self):
        self.assertEqual(transform_latitude_to_decimal_degrees(' 000000'), 0)

    def test_with_positive_latitude(self):
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees(' 474312'), 47.72, 2)
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees(' 085623'), 8.93972222, 8)

    def test_with_negative_latitude(self):
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees('-474312'), -47.72, 2)
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees('-085623'), -8.93972222, 8)

    def test_with_outof_range_latitude(self):
        with self.assertRaises(ValueError):
            transform_latitude_to_decimal_degrees('400000')


class TestTransformLongitudeToDecimalDegrees(TestCase):

    def test_zero_values(self):
        self.assertEqual(transform_longitude_to_decimal_degrees(' 000000'), 0)

    def test_with_positive_latitude(self):
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees(' 0974312'), -97.72, 2)
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees(' 1234349'), -123.73027778, 8)

    def test_with_negative_latitude(self):
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees('-0974312'), 97.72, 2)
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees('-1234349'), 123.73027778, 8)

    def test_with_out_of_range_longitude(self):
        with self.assertRaises(ValueError):
            transform_longitude_to_decimal_degrees('1000000')


class TestTransformLocationTo_DecimalLocation(TestCase):

    def test_with_unconvertable_datum(self):
        self.assertEqual(transform_location_to_decimal_location(' 374312    ', '-1234349    ', 'WGS84     '),
                         {'decimalLatitude' : None, 'decimalLongitude': None})

    def test_with_nad83_datum(self):
        result = transform_location_to_decimal_location(' 374312    ', ' 1234349    ', 'NAD83     ')
        self.assertAlmostEqual(result.get('decimalLatitude'), 37.72, 5)
        self.assertAlmostEqual(result.get('decimalLongitude'), -123.73027778, 8)

    def test_with_nad27_datum(self):
        result = transform_location_to_decimal_location(' 383009    ', ' 0814256    ', 'NAD27     ')
        self.assertAlmostEqual(result.get('decimalLatitude'), 38.5025922044846, 8)
        self.assertAlmostEqual(result.get('decimalLongitude'), -81.7154066249968, 8)

    def test_with_non_numeric_lat_lon(self):
        self.assertEqual(transform_location_to_decimal_location('AAA',  ' 0814256    ', 'NAD27     '),
                         {'decimalLatitude': None, 'decimalLongitude': None})
        self.assertEqual(transform_location_to_decimal_location(' 374312    ', 'AAA', 'NAD27     '),
                         {'decimalLatitude': None, 'decimalLongitude': None})

    def test_with_invalid_numeric_lat_lon(self):
        self.assertEqual(transform_location_to_decimal_location('400000', ' 0814256    ', 'NAD83     '),
                         {'decimalLatitude': None, 'decimalLongitude': None})
        self.assertEqual(transform_location_to_decimal_location(' 400000', '1000000', 'NAD83     '),
                         {'decimalLatitude': None, 'decimalLongitude': None})



