from datetime import datetime
import math

from django.contrib.gis.geos import Point
from django.db import IntegrityError

from vehicles import conf as vehicle_conf, models as vehicles_models


class InvalidLocation(ValueError):
    """
    Raised when a location is provided outside of the city boundaries.
    """

    def __init__(self, location):
        return super().__init__(
            '{0} is more than {1}km from {2}'.format(
                location,
                vehicle_conf.BOUNDARY_RADIUS_KM,
                vehicle_conf.CITY_CENTER
            )
        )


def register_vehicle(uuid: str) -> vehicles_models.Vehicle:
    """
    (Re)register the Vehicle with the given UUID.
    """
    try:
        vehicle, _ = vehicles_models.Vehicle.objects.update_or_create(
            id=uuid, active=False, defaults=dict(active=True)
        )
    except IntegrityError:
        raise ValueError('Vehicle already registered')
    else:
        return vehicle


def deregister_vehicle(vehicle: vehicles_models.Vehicle) -> None:
    """
    Deregister the given Vehicle instance.
    """
    if not vehicle.active:
        raise ValueError('Vehicle already deregistered')

    vehicle.active = False
    vehicle.current_location = None
    vehicle.current_bearing = None
    vehicle.save()


def update_location(
    vehicle: vehicles_models.Vehicle, location: Point, at: datetime
) -> vehicles_models.VehicleLocation:
    """
    Update the location of the given vehicle.

    If a previous location was set, the vehicle's bearing is also calculated
    from comparing it with the given location.
    """
    if not location_is_valid(location):
        raise InvalidLocation(location)

    # Store the current bearing on the vehicle if it had a previous location,
    # ensure that the latest update is after the previous
    if (
        vehicle.current_location and
        vehicle.last_update_at and
        vehicle.last_update_at < at
    ):
        vehicle.current_bearing = get_bearing_degrees(
            vehicle.current_location, location
        )

    vehicle.current_location = location
    vehicle.last_update_at = at
    vehicle.save()

    vehicles_models.VehicleLocation.objects.create(
        vehicle=vehicle, location=location, at=at
    )


def location_is_valid(location: Point) -> bool:
    """
    Return whether the given location is within the expected "city boundaries".
    """
    return vehicle_conf.CITY_POLYGON.contains(location)


def get_bearing_degrees(from_location: Point, to_location: Point) -> int:
    """
    Return the bearing expressed in degrees between the given points.

    Adapted from: http://bit.ly/2j8kYNA
    """
    from_lng, from_lat = from_location
    to_lng, to_lat = to_location

    lng_difference = to_lng - from_lng
    y = math.sin(lng_difference) * math.cos(to_lat)
    x = (
        math.cos(from_lat) * math.sin(to_lat) -
        math.sin(from_lat) * math.cos(to_lat) * math.cos(lng_difference)
    )

    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    return (bearing + 360) % 360
