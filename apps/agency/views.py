from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Agency, Driver, Bus
from .forms import AgencyRegistrationForm, DriverForm, BusForm
from .mixins import agency_required
from apps.accounts.models import User


def agency_register(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_agency_manager:
        try:
            request.user.agency
            return redirect('agency:dashboard')
        except Agency.DoesNotExist:
            pass
    if request.method == 'POST':
        form = AgencyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            agency = form.save(commit=False)
            agency.manager = request.user
            agency.save()
            request.user.role = 'agency'
            request.user.save()
            messages.success(request, 'Agency registered! Awaiting admin approval.')
            return redirect('agency:pending')
    else:
        form = AgencyRegistrationForm()
    return render(request, 'agency/register.html', {'form': form})


@login_required
def agency_pending(request):
    try:
        agency = request.user.agency
        if agency.is_approved:
            return redirect('agency:dashboard')
    except Agency.DoesNotExist:
        return redirect('agency:register')
    return render(request, 'agency/pending.html', {'agency': agency})


@agency_required
def agency_dashboard(request):
    agency = request.user.agency
    from apps.trips.models import Trip
    from apps.bookings.models import Booking
    from django.db.models import Sum, Count
    from datetime import date

    trips = Trip.objects.filter(agency=agency)
    today_bookings = Booking.objects.filter(
        trip__agency=agency,
        status='confirmed',
        booked_at__date=date.today()
    ).count()
    total_bookings = Booking.objects.filter(trip__agency=agency, status='confirmed').count()
    total_revenue = Booking.objects.filter(
        trip__agency=agency, status='confirmed'
    ).aggregate(total=Sum('total_price'))['total'] or 0

    from django.db.models import Q
    bus_revenues = agency.buses.annotate(
        revenue=Sum('trips__bookings__total_price', filter=Q(trips__bookings__status='confirmed')),
        trips_count=Count('trips', distinct=True),
        bookings_count=Count('trips__bookings', filter=Q(trips__bookings__status='confirmed'), distinct=True),
    ).order_by('-revenue', 'registration_number')

    for b in bus_revenues:
        b.revenue_amount = b.revenue or 0
        b.revenue_share = round((b.revenue_amount / total_revenue * 100), 1) if total_revenue > 0 else 0

    upcoming_trips = trips.filter(
        departure_datetime__gte=timezone.now(),
        status='scheduled'
    ).select_related('route__origin', 'route__destination', 'bus', 'driver')[:5]
    recent_bookings = Booking.objects.filter(
        trip__agency=agency
    ).select_related('passenger', 'trip__route__origin', 'trip__route__destination').order_by('-booked_at')[:10]

    return render(request, 'agency/dashboard.html', {
        'agency': agency,
        'total_trips': trips.count(),
        'active_buses': agency.buses.filter(status='active').count(),
        'total_drivers': agency.drivers.filter(status='active').count(),
        'today_bookings': today_bookings,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'bus_revenues': bus_revenues,
        'upcoming_trips': upcoming_trips,
        'recent_bookings': recent_bookings,
    })


# --- Driver Views ---

@agency_required
def driver_list(request):
    agency = request.user.agency
    drivers = agency.drivers.all()

    total_fleet_drivers = drivers.count()
    active_drivers_count = drivers.filter(status='active').count()
    total_assigned_trips = sum(d.total_trips_count for d in drivers)

    return render(request, 'agency/drivers/list.html', {
        'drivers': drivers,
        'agency': agency,
        'total_fleet_drivers': total_fleet_drivers,
        'active_drivers_count': active_drivers_count,
        'total_assigned_trips': total_assigned_trips,
    })


@agency_required
def driver_add(request):
    agency = request.user.agency
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.agency = agency
            driver.save()
            messages.success(request, f'Driver {driver.full_name} added successfully.')
            return redirect('agency:drivers')
    else:
        form = DriverForm()
    return render(request, 'agency/drivers/form.html', {'form': form, 'title': 'Add Driver'})


@agency_required
def driver_edit(request, pk):
    agency = request.user.agency
    driver = get_object_or_404(Driver, pk=pk, agency=agency)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, f'Driver {driver.full_name} updated.')
            return redirect('agency:drivers')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'agency/drivers/form.html', {'form': form, 'driver': driver, 'title': 'Edit Driver'})


@agency_required
def driver_delete(request, pk):
    agency = request.user.agency
    driver = get_object_or_404(Driver, pk=pk, agency=agency)
    if request.method == 'POST':
        name = driver.full_name
        driver.delete()
        messages.success(request, f'Driver {name} deleted.')
    return redirect('agency:drivers')


# --- Bus Views ---

@agency_required
def bus_list(request):
    agency = request.user.agency
    from apps.bookings.models import Booking
    from django.db.models import Sum, Count, Q

    buses = agency.buses.annotate(
        revenue=Sum('trips__bookings__total_price', filter=Q(trips__bookings__status='confirmed')),
        trips_count=Count('trips', distinct=True),
        bookings_count=Count('trips__bookings', filter=Q(trips__bookings__status='confirmed'), distinct=True),
    ).order_by('-revenue', '-created_at')

    total_fleet_revenue = sum((b.revenue or 0) for b in buses)
    total_fleet_bookings = sum((b.bookings_count or 0) for b in buses)
    total_fleet_trips = sum((b.trips_count or 0) for b in buses)

    for b in buses:
        b.revenue_amount = b.revenue or 0
        b.revenue_share = round((b.revenue_amount / total_fleet_revenue * 100), 1) if total_fleet_revenue > 0 else 0

    return render(request, 'agency/buses/list.html', {
        'buses': buses,
        'agency': agency,
        'total_fleet_revenue': total_fleet_revenue,
        'total_fleet_bookings': total_fleet_bookings,
        'total_fleet_trips': total_fleet_trips,
    })


@agency_required
def bus_add(request):
    agency = request.user.agency
    if request.method == 'POST':
        form = BusForm(request.POST, request.FILES)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.agency = agency
            bus.save()
            messages.success(request, f'Bus {bus.registration_number} added successfully.')
            return redirect('agency:buses')
    else:
        form = BusForm()
    return render(request, 'agency/buses/form.html', {'form': form, 'title': 'Add Bus'})


@agency_required
def bus_edit(request, pk):
    agency = request.user.agency
    bus = get_object_or_404(Bus, pk=pk, agency=agency)
    if request.method == 'POST':
        form = BusForm(request.POST, request.FILES, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bus {bus.registration_number} updated.')
            return redirect('agency:buses')
    else:
        form = BusForm(instance=bus)
    return render(request, 'agency/buses/form.html', {'form': form, 'bus': bus, 'title': 'Edit Bus'})


@agency_required
def bus_delete(request, pk):
    agency = request.user.agency
    bus = get_object_or_404(Bus, pk=pk, agency=agency)
    if request.method == 'POST':
        reg = bus.registration_number
        bus.delete()
        messages.success(request, f'Bus {reg} deleted.')
    return redirect('agency:buses')


@agency_required
def agency_bookings(request):
    from apps.bookings.models import Booking
    from django.db.models import Sum
    agency = request.user.agency
    bookings = Booking.objects.filter(
        trip__agency=agency
    ).select_related(
        'passenger',
        'trip__route__origin',
        'trip__route__destination',
        'trip__bus'
    ).order_by('-booked_at')

    # Calculate passenger travel history with this agency
    for b in bookings:
        b.passenger_agency_trips = Booking.objects.filter(
            trip__agency=agency,
            passenger=b.passenger,
            status='confirmed'
        ).count()

    total_bookings_count = bookings.count()
    confirmed_bookings_count = bookings.filter(status='confirmed').count()
    pending_bookings_count = bookings.filter(status='pending').count()
    total_agency_revenue = bookings.filter(status='confirmed').aggregate(t=Sum('total_price'))['t'] or 0

    return render(request, 'agency/bookings/list.html', {
        'bookings': bookings,
        'agency': agency,
        'total_bookings_count': total_bookings_count,
        'confirmed_bookings_count': confirmed_bookings_count,
        'pending_bookings_count': pending_bookings_count,
        'total_agency_revenue': total_agency_revenue,
    })
