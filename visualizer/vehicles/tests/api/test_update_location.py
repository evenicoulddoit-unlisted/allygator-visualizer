from datetime import datetime, timedelta

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils import timezone

from vehicles import (
    api as vehicles_api, conf as vehicles_conf, models as vehicles_models
)


class UpdateLocationTests(TestCase):
    """
    Unit tests for the update_location() API method.
    """

    def setUp(self):
        self.vehicle = vehicles_models.Vehicle.objects.create()
        self.dt = timezone.make_aware(datetime(2017, 12, 1))
        self.location_2 = vehicles_conf.CITY_CENTER.clone()
        self.location_2.y = vehicles_conf.CITY_CENTER.y - 0.01

    def test_raises_exception_given_invalid_location(self):
        with self.assertRaises(vehicles_api.InvalidLocation):
            vehicles_api.update_location(self.vehicle, Point(0, 0), self.dt)

    def test_sets_current_location_on_vehicle(self):
        vehicles_api.update_location(
            self.vehicle, vehicles_conf.CITY_CENTER, self.dt
        )
        self.vehicle.refresh_from_db()
        self.assertEqual(
            vehicles_conf.CITY_CENTER, self.vehicle.current_location
        )
        self.assertEqual(self.dt, self.vehicle.last_update_at)

    def test_updates_current_location_on_vehicle(self):
        dt_after = self.dt + timedelta(seconds=3)
        vehicles_api.update_location(
            self.vehicle, vehicles_conf.CITY_CENTER, self.dt
        )
        vehicles_api.update_location(self.vehicle, self.location_2, dt_after)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.location_2, self.vehicle.current_location)
        self.assertEqual(dt_after, self.vehicle.last_update_at)

    def test_adds_vehicle_location_entry(self):
        response = vehicles_api.update_location(
            self.vehicle, vehicles_conf.CITY_CENTER, self.dt
        )
        self.assertEqual(1, vehicles_models.VehicleLocation.objects.count())

        vehicle_location = vehicles_models.VehicleLocation.objects.get()
        self.assertEqual(vehicle_location.vehicle, self.vehicle)
        self.assertEqual(vehicles_conf.CITY_CENTER, vehicle_location.location)
        self.assertEqual(self.dt, vehicle_location.at)
        self.assertEqual(response, vehicle_location)

    def test_sets_bearing_when_previous_location(self):
        dt_after = self.dt + timedelta(seconds=3)
        vehicles_api.update_location(
            self.vehicle, vehicles_conf.CITY_CENTER, self.dt
        )
        vehicles_api.update_location(
            self.vehicle, self.location_2, dt_after
        )
        self.vehicle.refresh_from_db()
        self.assertEqual(180, self.vehicle.current_bearing)

    def test_does_not_set_bearing_when_previous_update_after_new(self):
        """
        Test that if the incoming update is before current, no bearing set.

        Given the requirements, it seems that the client is allowed to
        determine when the update occurred. It's therefore possible that a
        location update could be made with a date *earlier* than the one we
        currently hold.

        We could either do two things in this situation: ignore the update, or
        process it. Given the modelling, it seems that losing the bearing
        information in such a circumstance might be the best solution.
        """
        dt_before = self.dt - timedelta(seconds=3)
        vehicles_api.update_location(
            self.vehicle, vehicles_conf.CITY_CENTER, self.dt
        )
        vehicles_api.update_location(
            self.vehicle, self.location_2, dt_before
        )
        self.vehicle.refresh_from_db()

        # The latest update still sets the other fields
        self.assertEqual(self.location_2, self.vehicle.current_location)
        self.assertEqual(dt_before, self.vehicle.last_update_at)

        # But the bearing is not set
        self.assertIsNone(self.vehicle.current_bearing)
