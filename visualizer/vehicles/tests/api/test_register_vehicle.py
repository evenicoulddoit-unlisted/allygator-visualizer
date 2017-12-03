from django.test import TestCase

from vehicles import api as vehicles_api, models as vehicles_models


class RegisterVehicleTests(TestCase):
    """
    Unit tests for the register_vehicle() API method.
    """

    def test_creates_and_returns_active_vehicle(self):
        vehicle = vehicles_api.register_vehicle('a')
        self.assertIsInstance(vehicle, vehicles_models.Vehicle)
        self.assertEqual(1, vehicles_models.Vehicle.objects.count())
        self.assertEqual('a', vehicle.id)
        self.assertTrue(vehicle.active)

    def test_creates_multiple_vehicles(self):
        vehicles_api.register_vehicle('a')
        vehicles_api.register_vehicle('b')
        self.assertEqual(2, vehicles_models.Vehicle.objects.count())
        self.assertEqual(
            {'a', 'b'},
            set(vehicles_models.Vehicle.objects.values_list('id', flat=True))
        )

    def test_reactivates_existing_inactive_vehicle(self):
        existing = vehicles_models.Vehicle.objects.create(
            id='a', active=False
        )
        response = vehicles_api.register_vehicle('a')
        existing.refresh_from_db()
        self.assertEqual(existing, response)
        self.assertTrue(existing.active)

    def test_raises_exception_when_already_active(self):
        vehicles_api.register_vehicle('a')

        with self.assertRaisesRegexp(ValueError, 'already registered'):
            vehicles_api.register_vehicle('a')
