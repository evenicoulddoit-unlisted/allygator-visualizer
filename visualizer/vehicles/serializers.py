from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from vehicles import api as vehicles_api, models as vehicles_models


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serialize a Vehicle instance.

    When a Vehicle is registered (created), the only input required is it's
    UUID. All other fields are read-only.
    """
    id = serializers.UUIDField(required=True)
    lat = serializers.FloatField(read_only=True, source='current_location.y')
    lng = serializers.FloatField(read_only=True, source='current_location.x')
    bearing = serializers.IntegerField(
        read_only=True, source='current_bearing'
    )

    class Meta:
        model = vehicles_models.Vehicle
        fields = ('id', 'active', 'lat', 'lng', 'bearing', 'last_update_at')

    def create(self, validated_data):
        """
        Register the vehicle via the private API
        """
        return vehicles_api.register_vehicle(validated_data['id'])


class VehicleLocationSerializer(serializers.ModelSerializer):
    """
    Serialize a VehicleLocation instance.
    """
    lat = serializers.FloatField(write_only=True)
    lng = serializers.FloatField(write_only=True)

    class Meta:
        model = vehicles_models.VehicleLocation
        fields = ('at', 'lat', 'lng')

    def validate(self, attrs):
        """
        Combine the latitude and longitude into a Point, and validate.
        """
        location = vehicles_api.point_from_lat_lng(
            attrs.pop('lat'), attrs.pop('lng')
        )

        try:
            vehicles_api.validate_location(location)
        except vehicles_api.InvalidLocation as e:
            raise ValidationError(str(e))

        attrs.update(location=location)
        return attrs

    def create(self, validated_data):
        """
        Save the model via the private API.
        """
        return vehicles_api.update_location(
            self.context['vehicle'],
            validated_data['location'], validated_data['at']
        )
