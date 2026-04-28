from django.urls import path
from . import api_views

urlpatterns = [
    path('seats/<uuid:trip_id>/', api_views.seat_availability, name='api_seats'),
    path('cities/', api_views.city_list, name='api_cities'),
]
