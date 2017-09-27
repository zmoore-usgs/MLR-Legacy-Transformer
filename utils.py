from pyproj import Proj, transform

nad83_proj = Proj(init='epsg:4269')
nad27_proj = Proj(init='epsg:4267')

def transform_to_decimal_degrees(degrees, minutes, seconds):
    fdegrees = float(degrees)
    abs_result = abs(fdegrees) + float(minutes) / 60 + float(seconds) / 3600
    return abs_result if fdegrees > 0 else -abs_result

def transform_latitude_to_decimal_degrees(angle):
    return transform_to_decimal_degrees(angle[0:3], angle[3:5], angle[5:])

def transform_longitude_to_decimal_degrees(angle):
    return -transform_to_decimal_degrees(angle[0:4], angle[4:6], angle[6:])

