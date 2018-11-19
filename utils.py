from pyproj import Proj, transform
from app import application

nad83_proj = Proj('+init=EPSG:4269')
nad27_proj = Proj('+init=EPSG:4267')

DATUM_TO_PROJ = {
    'NAD83' : nad83_proj,
    'NAD27' : nad27_proj,
}

def transform_to_decimal_degrees(degrees, minutes, seconds):
    fdegrees = float(degrees)
    abs_result = abs(fdegrees) + float(minutes) / 60 + float(seconds) / 3600
    return abs_result if fdegrees > 0 else -abs_result

def transform_latitude_to_decimal_degrees(angle):
    result = transform_to_decimal_degrees(angle[0:3], angle[3:5], angle[5:])
    if result > 90.0 or result < -90.0:
        raise ValueError('Latitude angle ' + str(angle) + ' is not in the inclusive range of (-90, 90)')
    return result

def transform_longitude_to_decimal_degrees(angle):
    result = -transform_to_decimal_degrees(angle[0:4], angle[4:6], angle[6:])
    if result > 180.0 or result < -180.0:
        raise ValueError('Longitude angle ' + str(angle) + ' is not in the inclusive range of (-180, 180)')
    return result

def transform_location_to_decimal_location(latitude, longitude, coord_datum):
    datum = coord_datum.rstrip()
    if datum in DATUM_TO_PROJ:
        try:
            dlat = transform_latitude_to_decimal_degrees(latitude)
            dlon = transform_longitude_to_decimal_degrees(longitude)
        except ValueError as err:
            dlat, dlon = None, None
            application.logger.error("An error occurred while transforming lat/lon to decimal degrees: "
                + str(err))
        else:
            if datum != 'NAD83':
                dlon, dlat = transform(DATUM_TO_PROJ[datum], nad83_proj, dlon, dlat)

    else:
        dlat, dlon = None, None

    return {
        'decimalLatitude' : dlat,
        'decimalLongitude' : dlon
    }
