from django.contrib.gis.geos import Point
from django.test import TestCase

from vehicles import api as vehicles_api, models as vehicles_models


class DeregisterVehicleTests(TestCase):
    """
    Unit tests for the deregister_vehicle() API method.
    """

    def test_removes_active_flag(self):
        vehicle = vehicles_models.Vehicle.objects.create(active=True)
        vehicles_api.deregister_vehicle(vehicle)
        vehicle.refresh_from_db()
        self.assertFalse(vehicle.active)

    def test_unsets_current_location_and_bearing(self):
        """
        Removes the current location and bearing.

        If the vehicle later reactivates, we don't want to use it's previous
        location to determine the new bearing.
        """
        vehicle = vehicles_models.Vehicle.objects.create(
            active=True,
            current_location=Point(1, 2),
            current_bearing=90,
        )
        vehicles_api.deregister_vehicle(vehicle)
        vehicle.refresh_from_db()
        self.assertIsNone(vehicle.current_location)
        self.assertIsNone(vehicle.current_bearing)

    def test_raises_exception_when_already_inactive(self):
        vehicle = vehicles_models.Vehicle.objects.create(active=False)

        with self.assertRaisesRegexp(ValueError, 'already deregistered'):
            vehicles_api.deregister_vehicle(vehicle)
