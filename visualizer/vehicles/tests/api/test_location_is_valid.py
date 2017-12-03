from django.contrib.gis.geos import Point
from django.test import TestCase

from vehicles import api as vehicles_api, conf as vehicles_conf


# Valid location
LOC_VABALI_SPA = Point(13.362, 52.529, srid=vehicles_conf.SRID_DEFAULT)

# Invalid locations
LOC_WICLEF63_CASIO = Point(13.341, 52.531, srid=vehicles_conf.SRID_DEFAULT)
LOC_FENNPFUFL_PARK = Point(13.462, 52.531, srid=vehicles_conf.SRID_DEFAULT)
LOC_BURGERPARK_PANKOW = Point(13.396, 52.568, srid=vehicles_conf.SRID_DEFAULT)
LOC_TEMPELHOFER = Point(13.396, 52.485, srid=vehicles_conf.SRID_DEFAULT)


class LocationIsValidTests(TestCase):
    """
    Unit tests for the location_is_valid() API method.
    """

    def test_city_center_valid(self):
        self.assertTrue(
            vehicles_api.location_is_valid(vehicles_conf.CITY_CENTER)
        )

    def test_huge_distance_away_invalid(self):
        self.assertFalse(vehicles_api.location_is_valid(Point(0, 0)))

    def test_3km_away_valid(self):
        self.assertTrue(vehicles_api.location_is_valid(LOC_VABALI_SPA))

    def test_over_3km_away_west_invalid(self):
        self.assertFalse(vehicles_api.location_is_valid(LOC_WICLEF63_CASIO))

    def test_over_3km_away_east_invalid(self):
        self.assertFalse(vehicles_api.location_is_valid(LOC_FENNPFUFL_PARK))

    def test_over_3km_away_north_invalid(self):
        self.assertFalse(vehicles_api.location_is_valid(LOC_BURGERPARK_PANKOW))

    def test_over_3km_away_south_invalid(self):
        self.assertFalse(vehicles_api.location_is_valid(LOC_TEMPELHOFER))
