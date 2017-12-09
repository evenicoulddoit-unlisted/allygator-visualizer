"""
Configuration for the Vehicles app.

Here we define the "city boundaries", which are used to invalidate updates
from locations which are a distant proximity from the Door2Door office.
"""
from django.contrib.gis.geos import Point


# Spacial references
SRID_DEFAULT = 4326
SRID_BERLIN = 3068

# The center location the city
CITY_CENTER_LNG = 13.403
CITY_CENTER_LAT = 52.53

CITY_CENTER = Point(CITY_CENTER_LNG, CITY_CENTER_LAT)
CITY_CENTER.srid = 4326

# The radius size of the city
BOUNDARY_RADIUS_KM = 3.5


# The city's polygon as expressed in lat/lon coordinates
def get_city_polygon():
    return (
        CITY_CENTER
        .transform(SRID_BERLIN, clone=True)
        .buffer(BOUNDARY_RADIUS_KM * 1000)
        .transform(SRID_DEFAULT, clone=True)
    )
