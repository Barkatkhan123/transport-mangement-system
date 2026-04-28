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
        'upcoming_trips': upcoming_trips,
        'recent_bookings': recent_bookings,
    })


# --- Driver Views ---

@agency_required
def driver_list(request):
    agency = request.user.agency
    drivers = agency.drivers.all()
    return render(request, 'agency/drivers/list.html', {'drivers': drivers, 'agency': agency})


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
    buses = agency.buses.all()
    return render(request, 'agency/buses/list.html', {'buses': buses, 'agency': agency})


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
    agency = request.user.agency
    bookings = Booking.objects.filter(
        trip__agency=agency
    ).select_related('passenger', 'trip__route__origin', 'trip__route__destination').order_by('-booked_at')
    return render(request, 'agency/bookings/list.html', {'bookings': bookings, 'agency': agency})
