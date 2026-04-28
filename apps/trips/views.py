from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Trip, City, Route, Seat
from .forms import TripSearchForm, TripForm, RouteForm
from apps.agency.mixins import agency_required


def home(request):
    form = TripSearchForm()
    cities = City.objects.all()
    featured_trips = Trip.objects.filter(
        status='scheduled',
        departure_datetime__gte=timezone.now()
    ).select_related('route__origin', 'route__destination', 'agency', 'bus').order_by('departure_datetime')[:6]
    return render(request, 'passenger/home.html', {
        'form': form,
        'cities': cities,
        'featured_trips': featured_trips,
    })


def search_trips(request):
    form = TripSearchForm(request.GET or None)
    trips = []
    search_params = {}

    if form.is_valid():
        origin = form.cleaned_data['origin']
        destination = form.cleaned_data['destination']
        travel_date = form.cleaned_data['travel_date']
        passengers = form.cleaned_data['passengers']

        trips = Trip.objects.filter(
            route__origin=origin,
            route__destination=destination,
            departure_datetime__date=travel_date,
            status='scheduled'
        ).select_related(
            'route__origin', 'route__destination', 'agency', 'bus', 'driver'
        ).prefetch_related('seats').order_by('departure_datetime')

        trips = [t for t in trips if t.available_seats_count >= passengers]

        search_params = {
            'origin': origin,
            'destination': destination,
            'travel_date': travel_date,
            'passengers': passengers,
        }

    return render(request, 'passenger/search_results.html', {
        'form': form,
        'trips': trips,
        'search_params': search_params,
    })


def trip_detail(request, pk):
    trip = get_object_or_404(
        Trip.objects.select_related(
            'route__origin', 'route__destination', 'agency', 'bus', 'driver'
        ).prefetch_related('seats'),
        pk=pk,
        status='scheduled'
    )
    seats = trip.seats.all().order_by('row_number', 'column_number')
    passengers = request.GET.get('passengers', 1)

    seat_rows = {}
    for seat in seats:
        if seat.row_number not in seat_rows:
            seat_rows[seat.row_number] = []
        seat_rows[seat.row_number].append(seat)

    return render(request, 'passenger/trip_detail.html', {
        'trip': trip,
        'seat_rows': seat_rows,
        'passengers': int(passengers),
    })


# --- Agency Trip Management ---

@agency_required
def agency_trips(request):
    agency = request.user.agency
    trips = Trip.objects.filter(agency=agency).select_related(
        'route__origin', 'route__destination', 'bus', 'driver'
    ).order_by('-departure_datetime')
    return render(request, 'agency/trips/list.html', {'trips': trips, 'agency': agency})


@agency_required
def trip_schedule(request):
    agency = request.user.agency
    if request.method == 'POST':
        form = TripForm(agency=agency, data=request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.agency = agency
            trip.save()
            messages.success(request, f'Trip scheduled: {trip}')
            return redirect('agency:trips')
    else:
        form = TripForm(agency=agency)
    routes = Route.objects.select_related('origin', 'destination').all()
    return render(request, 'agency/trips/form.html', {
        'form': form,
        'routes': routes,
        'title': 'Schedule Trip',
    })


@agency_required
def trip_edit(request, pk):
    agency = request.user.agency
    trip = get_object_or_404(Trip, pk=pk, agency=agency)
    if request.method == 'POST':
        form = TripForm(agency=agency, data=request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated.')
            return redirect('agency:trips')
    else:
        form = TripForm(agency=agency, instance=trip)
    return render(request, 'agency/trips/form.html', {'form': form, 'trip': trip, 'title': 'Edit Trip'})


@agency_required
def trip_cancel(request, pk):
    agency = request.user.agency
    trip = get_object_or_404(Trip, pk=pk, agency=agency)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        trip.status = 'cancelled'
        trip.cancellation_reason = reason
        trip.save()
        messages.warning(request, f'Trip cancelled: {trip}')
    return redirect('agency:trips')


@agency_required
def trip_detail_agency(request, pk):
    agency = request.user.agency
    trip = get_object_or_404(
        Trip.objects.select_related('route__origin', 'route__destination', 'bus', 'driver'),
        pk=pk, agency=agency
    )
    from apps.bookings.models import Booking
    bookings = Booking.objects.filter(trip=trip).select_related('passenger').prefetch_related('seats').order_by('-booked_at')
    return render(request, 'agency/trips/detail.html', {
        'trip': trip,
        'bookings': bookings,
        'agency': agency,
    })


@agency_required
def route_list(request):
    agency = request.user.agency
    routes = Route.objects.select_related('origin', 'destination').all()
    return render(request, 'agency/routes/list.html', {'routes': routes, 'agency': agency})


@agency_required
def route_add(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route added.')
            return redirect('agency:routes')
    else:
        form = RouteForm()
    return render(request, 'agency/routes/form.html', {'form': form, 'title': 'Add Route'})
