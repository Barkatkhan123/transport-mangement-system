from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('confirm/<uuid:trip_id>/', views.booking_confirm, name='booking_confirm'),
    path('create/', views.create_booking, name='create_booking'),
    path('payment/<uuid:booking_id>/', views.payment_view, name='payment'),
    path('ticket/<uuid:ticket_number>/', views.ticket_view, name='ticket_view'),
    path('cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
