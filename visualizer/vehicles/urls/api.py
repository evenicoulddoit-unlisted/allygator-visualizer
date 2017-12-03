from django.urls import include, path

from vehicles.views import api as vehicles_views_api


app_name = 'vehicles'
urlpatterns = [
    path(
        '',
        vehicles_views_api.ListRegisterVehicle.as_view(),
        name='list-register'
    ),
    path(
        '/<uuid:id>',
        include([
            path(
                '', vehicles_views_api.DeregisterVehicle.as_view(),
                name='deregister'
            ),
            path(
                '/locations', vehicles_views_api.LocationUpdate.as_view(),
                name='location-update'
            )
        ]),
    ),
]
