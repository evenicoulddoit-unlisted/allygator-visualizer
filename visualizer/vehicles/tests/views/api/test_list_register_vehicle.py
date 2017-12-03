from datetime import datetime
import uuid

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vehicles import models as vehicles_models


class ListRegisterVehicleTests(TestCase):
    """
    Integration tests for the ListRegisterVehicle API view.
    """
    url = 'vehicles:list-register'

    def setUp(self):
        self.client = APIClient()

    def test_post_creates_vehicle_with_given_uuid(self):
        """
        Test that posting a valid UUID for a new vehicle creates it.
        """
        id_ = uuid.uuid4()
        response = self.client.post(
            reverse(self.url),
            data=dict(id=id_)
        )

        # A 204 no content response is returned
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(b'', response.render().content)

        # The vehicle is created
        self.assertEqual(1, vehicles_models.Vehicle.objects.count())
        vehicle = vehicles_models.Vehicle.objects.get()
        self.assertEqual(id_, vehicle.id)
        self.assertTrue(vehicle.active)

    def test_post_reactivates_existing_vehicle_with_given_uuid(self):
        """
        Test that posting a valid UUID for an existing vehicle activates it.
        """
        id_ = uuid.uuid4()
        vehicle = vehicles_models.Vehicle.objects.create(id=id_, active=False)

        response = self.client.post(
            reverse(self.url),
            data=dict(id=id_)
        )

        # A 204 no content response is returned
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(b'', response.render().content)

        # The existing vehicle is re-activated
        vehicle.refresh_from_db()
        self.assertEqual(1, vehicles_models.Vehicle.objects.count())
        self.assertTrue(vehicle.active)

    def test_get_lists_existing_vehicles(self):
        """
        Test that GET requests return the serialized vehicles.

        TODO: Test all serialized attributes.
        """
        vehicle_a = vehicles_models.Vehicle.objects.create(
            id=uuid.uuid4(),
            current_location=Point(1, 2),
            current_bearing=90,
            last_update_at=timezone.make_aware(datetime(2017, 12, 1, 12)),
        )
        vehicle_b = vehicles_models.Vehicle.objects.create(
            id=uuid.uuid4(),
            current_location=Point(3, 4),
            current_bearing=180,
            last_update_at=timezone.make_aware(datetime(2017, 12, 1, 13)),
        )

        response = self.client.get(reverse(self.url))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertIsInstance(data, list)
        self.assertEqual(2, len(data))
        self.assertEqual(
            {str(vehicle_a.id), str(vehicle_b.id)},
            set([vehicle['id'] for vehicle in data])
        )
