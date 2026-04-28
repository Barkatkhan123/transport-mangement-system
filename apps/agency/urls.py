from django.urls import path
from . import views
from apps.trips.views import (
    agency_trips, trip_schedule, trip_edit, trip_cancel,
    trip_detail_agency, route_list, route_add
)

app_name = 'agency'

urlpatterns = [
    path('register/', views.agency_register, name='register'),
    path('pending/', views.agency_pending, name='pending'),
    path('dashboard/', views.agency_dashboard, name='dashboard'),

    path('drivers/', views.driver_list, name='drivers'),
    path('drivers/add/', views.driver_add, name='driver_add'),
    path('drivers/<uuid:pk>/edit/', views.driver_edit, name='driver_edit'),
    path('drivers/<uuid:pk>/delete/', views.driver_delete, name='driver_delete'),

    path('buses/', views.bus_list, name='buses'),
    path('buses/add/', views.bus_add, name='bus_add'),
    path('buses/<uuid:pk>/edit/', views.bus_edit, name='bus_edit'),
    path('buses/<uuid:pk>/delete/', views.bus_delete, name='bus_delete'),

    path('trips/', agency_trips, name='trips'),
    path('trips/schedule/', trip_schedule, name='trip_schedule'),
    path('trips/<uuid:pk>/edit/', trip_edit, name='trip_edit'),
    path('trips/<uuid:pk>/cancel/', trip_cancel, name='trip_cancel'),
    path('trips/<uuid:pk>/detail/', trip_detail_agency, name='trip_detail'),

    path('routes/', route_list, name='routes'),
    path('routes/add/', route_add, name='route_add'),

    path('bookings/', views.agency_bookings, name='bookings'),
]
