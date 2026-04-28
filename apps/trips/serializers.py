from rest_framework import serializers
from .models import Seat, Trip, City


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'row_number', 'column_number',
                  'seat_type', 'is_booked', 'gender_restriction']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'province']


class TripListSerializer(serializers.ModelSerializer):
    origin = serializers.CharField(source='route.origin.name')
    destination = serializers.CharField(source='route.destination.name')
    duration = serializers.CharField(source='route.duration_display')
    agency_name = serializers.CharField(source='agency.name')
    available_seats = serializers.IntegerField(source='available_seats_count')

    class Meta:
        model = Trip
        fields = ['id', 'origin', 'destination', 'departure_datetime', 'arrival_datetime',
                  'base_price', 'status', 'duration', 'agency_name', 'available_seats']
