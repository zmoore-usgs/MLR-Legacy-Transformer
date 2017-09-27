from pyproj import Proj, transform

nad83_proj = Proj('+init=EPSG:4269')
nad27_proj = Proj('+init=EPSG:4267')
oldhi_proj = Proj('+init=EPSG:3565')

DATUM_TO_PROJ = {
    'NAD83     ' : nad83_proj,
    'NAD27     ' : nad27_proj,
}

def transform_to_decimal_degrees(degrees, minutes, seconds):
    fdegrees = float(degrees)
    abs_result = abs(fdegrees) + float(minutes) / 60 + float(seconds) / 3600
    return abs_result if fdegrees > 0 else -abs_result

def transform_latitude_to_decimal_degrees(angle):
    return transform_to_decimal_degrees(angle[0:3], angle[3:5], angle[5:])

def transform_longitude_to_decimal_degrees(angle):
    return -transform_to_decimal_degrees(angle[0:4], angle[4:6], angle[6:])

def transform_location_to_decimal_location(latitude, longitude, coord_datum):
    if coord_datum in DATUM_TO_PROJ:
        dlat = transform_latitude_to_decimal_degrees(latitude)
        dlon = transform_longitude_to_decimal_degrees(longitude)

        if coord_datum != 'NAD83     ':
            dlon, dlat = transform(DATUM_TO_PROJ[coord_datum], nad83_proj, dlon, dlat)

    else:
        dlat = None
        dlon = None

    return {
        'decimalLatitude' : dlat,
        'decimalLongitude' : dlon
    }
