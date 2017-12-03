from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListCreateAPIView
)
from rest_framework.response import Response

from vehicles import (
    api as vehicles_api, models as vehicles_models,
    serializers as vehicles_serializers
)


class VehicleAPIMixin:
    """
    Requirements ask for 204 empty responses.
    """
    queryset = vehicles_models.Vehicle.objects.all()
    lookup_url_kwarg = 'id'

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=204)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=204)


class ListRegisterVehicle(VehicleAPIMixin, ListCreateAPIView):
    """
    View to allow registering new vehicles and listing all existing ones.
    """
    serializer_class = vehicles_serializers.VehicleSerializer


class DeregisterVehicle(VehicleAPIMixin, DestroyAPIView):
    """
    View to deregister active vehicles.
    """

    def perform_destroy(self, instance):
        vehicles_api.deregister_vehicle(instance)


class LocationUpdate(VehicleAPIMixin, CreateAPIView):
    """
    View to provide location updates to active vehicles.
    """

    serializer_class = vehicles_serializers.VehicleLocationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(vehicle=self.get_object())
        return context
