import uuid

from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse

from vehicles import models as vehicles_models


class DeregisterVehicleTests(TestCase):
    """
    Integration tests for the DeregisterVehicle API view.
    """
    url = 'vehicles:deregister'

    def setUp(self):
        self.client = APIClient()

    def test_post_deregisters_vehicle_with_given_uuid(self):
        """
        Test that DELETEing with the UUID of a vehicle deregisters it.
        """
        vehicle_a = vehicles_models.Vehicle.objects.create(id=uuid.uuid4())
        vehicle_b = vehicles_models.Vehicle.objects.create(id=uuid.uuid4())

        url = reverse(self.url, kwargs=dict(id=vehicle_a.id))
        response = self.client.delete(url)

        # A 204 no content response is returned
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(b'', response.render().content)

        # Both vehicles still exist, but A is deregistered
        self.assertEqual(2, vehicles_models.Vehicle.objects.count())
        vehicle_a.refresh_from_db()
        vehicle_b.refresh_from_db()
        self.assertFalse(vehicle_a.active)
        self.assertTrue(vehicle_b.active)
