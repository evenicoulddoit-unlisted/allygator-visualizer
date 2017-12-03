from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vehicles import conf as vehicles_conf, models as vehicles_models


class LocationUpdateTests(TestCase):
    """
    Integration tests for the LocationUpdate API view.
    """
    url = 'vehicles:location-update'

    def setUp(self):
        self.client = APIClient()
        self.vehicle_a = vehicles_models.Vehicle.objects.create()
        self.vehicle_b = vehicles_models.Vehicle.objects.create()

    def test_post_sets_current_location_and_archives_record(self):
        """
        Test that location updates are stored against the correct vehicle.
        """
        dt = timezone.make_aware(datetime(2017, 12, 1, 11, 22, 33))
        url = reverse(self.url, kwargs=dict(id=self.vehicle_a.id))
        response = self.client.post(
            url,
            dict(
                lat=vehicles_conf.CITY_CENTER_LAT,
                lng=vehicles_conf.CITY_CENTER_LNG,
                at='2017-12-01T10:22:33Z',
            ),
        )

        # A 204 no content response is returned
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(b'', response.render().content)

        self.vehicle_a.refresh_from_db()
        self.vehicle_b.refresh_from_db()

        # Vehicle A is updated with the given location
        self.assertEqual(
            vehicles_conf.CITY_CENTER, self.vehicle_a.current_location
        )
        self.assertEqual(dt, self.vehicle_a.last_update_at)

        # Vehicle B is *not* updated
        self.assertIsNone(self.vehicle_b.current_location)
        self.assertIsNone(self.vehicle_b.last_update_at)

        # A VehicleLocation is stored for later data-analysis
        self.assertEqual(1, vehicles_models.VehicleLocation.objects.count())
        vehicle_location = vehicles_models.VehicleLocation.objects.get()
        self.assertEqual(self.vehicle_a, vehicle_location.vehicle)
        self.assertEqual(vehicles_conf.CITY_CENTER, vehicle_location.location)
        self.assertEqual(dt, vehicle_location.at)

    def test_rejects_updates_out_of_city_boundary(self):
        """
        Test that location updates outside of the city are not recorded.
        """
        url = reverse(self.url, kwargs=dict(id=self.vehicle_a.id))
        response = self.client.post(
            url, dict(lat=1, lng=2, at='2017-12-01T10:22:33Z'),
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.vehicle_a.refresh_from_db()
        self.assertIsNone(self.vehicle_a.current_location)
        self.assertFalse(vehicles_models.VehicleLocation.objects.exists())
