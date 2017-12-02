from django.contrib.gis.geos import Point

from vehicles import models as vehicles_models


def register_vehicle(uuid: str) -> vehicles_models.Vehicle:
    """
    (Re)register the Vehicle with the given UUID.
    """
    pass


def deregister_vehicle(vehicle: vehicles_models.Vehicle) -> None:
    """
    Deregister the given Vehicle instance.
    """
    pass


def update_location(
    vehicle: vehicles_models.Vehicle, location: Point
) -> vehicles_models.VehicleLocation:
    """
    Update the location of the given vehicle.

    If a previous location was set, the vehicle's bearing is also calculated
    from comparing it with the given location.
    """
    pass


def location_is_valid(location: Point) -> bool:
    """
    Return whether the given location is within the expected "city boundaries".
    """
    pass
