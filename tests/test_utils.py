
from unittest import TestCase

from utils import transform_to_decimal_degrees, transform_latitude_to_decimal_degrees, transform_longitude_to_decimal_degrees

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
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees(' 974312'), 97.72, 2)
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees(' 085623'), 8.93972222, 8)

    def test_with_negative_latitude(self):
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees('-974312'), -97.72, 2)
        self.assertAlmostEqual(transform_latitude_to_decimal_degrees('-085623'), -8.93972222, 8)


class TestTransformLongitudeToDecimalDegrees(TestCase):

    def test_zero_values(self):
        self.assertEqual(transform_longitude_to_decimal_degrees(' 000000'), 0)

    def test_with_positive_latitude(self):
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees(' 0974312'), -97.72, 2)
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees(' 1234349'), -123.73027778, 8)

    def test_with_negative_latitude(self):
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees('-0974312'), 97.72, 2)
        self.assertAlmostEqual(transform_longitude_to_decimal_degrees('-1234349'), 123.73027778, 8)
