import uuid

from django.test import TestCase

from vehicles import api as vehicles_api, models as vehicles_models


class RegisterVehicleTests(TestCase):
    """
    Unit tests for the register_vehicle() API method.
    """

    def test_creates_and_returns_active_vehicle(self):
        id_ = uuid.uuid4()
        vehicle = vehicles_api.register_vehicle(id_)
        self.assertIsInstance(vehicle, vehicles_models.Vehicle)
        self.assertEqual(1, vehicles_models.Vehicle.objects.count())
        self.assertEqual(id_, vehicle.id)
        self.assertTrue(vehicle.active)

    def test_creates_multiple_vehicles(self):
        id_a = uuid.uuid4()
        id_b = uuid.uuid4()
        vehicles_api.register_vehicle(id_a)
        vehicles_api.register_vehicle(id_b)
        self.assertEqual(2, vehicles_models.Vehicle.objects.count())
        self.assertEqual(
            {id_a, id_b},
            set(vehicles_models.Vehicle.objects.values_list('id', flat=True))
        )

    def test_reactivates_existing_inactive_vehicle(self):
        id_ = uuid.uuid4()
        existing = vehicles_models.Vehicle.objects.create(id=id_, active=False)
        response = vehicles_api.register_vehicle(id_)
        existing.refresh_from_db()
        self.assertEqual(existing, response)
        self.assertTrue(existing.active)

    def test_raises_exception_when_already_active(self):
        id_ = uuid.uuid4()
        vehicles_api.register_vehicle(id_)

        with self.assertRaisesRegexp(ValueError, 'already registered'):
            vehicles_api.register_vehicle(id_)
