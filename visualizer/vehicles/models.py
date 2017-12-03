from django.contrib.gis.db import models


class Vehicle(models.Model):
    """
    Model to store vehicle information and location details.
    """
    id = models.CharField(
        primary_key=True, max_length=36,
        help_text='Custom primary key represented by a UUID'
    )
    active = models.BooleanField(
        default=True, db_index=True,
        help_text='Whether the vehicle in active service'
    )
    current_location = models.PointField(
        null=True, blank=True,
        help_text='The coordinates representing the vehicles current location'
    )
    current_bearing = models.IntegerField(
        null=True, blank=True,
        help_text=(
            'The current bearing (direction of travel, in degrees) of the '
            'vehicle'
        )
    )
    last_update_at = models.DateTimeField(
        null=True, blank=True,
        help_text='When the vehicle last reported its location'
    )


class VehicleLocation(models.Model):
    """
    Model to store each report of a Vehicle's location.
    """
    vehicle = models.ForeignKey(
        'vehicles.Vehicle', on_delete=models.PROTECT,
        related_name='location_updates',
        db_index=False,
    )
    location = models.PointField()
    at = models.DateTimeField()
