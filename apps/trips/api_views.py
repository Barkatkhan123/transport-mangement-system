from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Trip, Seat, City
from .serializers import SeatSerializer, CitySerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def seat_availability(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    seats = trip.seats.all().order_by('row_number', 'column_number')
    serializer = SeatSerializer(seats, many=True)
    return Response({
        'trip_id': str(trip_id),
        'total_seats': trip.total_seats_count,
        'available_seats': trip.available_seats_count,
        'seats': serializer.data,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def city_list(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)
