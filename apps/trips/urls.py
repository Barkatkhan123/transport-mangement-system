from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_trips, name='search_trips'),
    path('trip/<uuid:pk>/', views.trip_detail, name='trip_detail'),
]

agency_trip_urlpatterns = [
    path('trips/', views.agency_trips, name='trips'),
    path('trips/schedule/', views.trip_schedule, name='trip_schedule'),
    path('trips/<uuid:pk>/edit/', views.trip_edit, name='trip_edit'),
    path('trips/<uuid:pk>/cancel/', views.trip_cancel, name='trip_cancel'),
    path('trips/<uuid:pk>/detail/', views.trip_detail_agency, name='trip_detail'),
    path('routes/', views.route_list, name='routes'),
    path('routes/add/', views.route_add, name='route_add'),
]
