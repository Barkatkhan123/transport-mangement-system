from django.contrib import admin
from .models import City, Route, Trip, Seat


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name',)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance_km', 'duration_display_admin')
    search_fields = ('origin__name', 'destination__name')

    def duration_display_admin(self, obj):
        return obj.duration_display
    duration_display_admin.short_description = 'Duration'


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'agency', 'bus', 'driver', 'departure_datetime', 'status', 'base_price')
    list_filter = ('status', 'agency')
    search_fields = ('route__origin__name', 'route__destination__name')
    date_hierarchy = 'departure_datetime'
    actions = ['cancel_trips']

    def cancel_trips(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_trips.short_description = 'Cancel selected trips'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'trip', 'seat_type', 'is_booked')
    list_filter = ('is_booked', 'seat_type')
