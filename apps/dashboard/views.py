from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


def admin_required(view_func):
    from functools import wraps
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_user:
            messages.error(request, 'Admin access required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    from apps.accounts.models import User
    from apps.agency.models import Agency
    from apps.trips.models import Trip
    from apps.bookings.models import Booking
    from django.db.models import Sum, Count
    from datetime import date

    stats = {
        'total_users': User.objects.filter(role='passenger').count(),
        'total_agencies': Agency.objects.filter(status='approved').count(),
        'pending_agencies': Agency.objects.filter(status='pending').count(),
        'total_trips': Trip.objects.count(),
        'active_trips': Trip.objects.filter(status='scheduled').count(),
        'total_bookings': Booking.objects.filter(status='confirmed').count(),
        'today_bookings': Booking.objects.filter(status='confirmed', booked_at__date=date.today()).count(),
        'total_revenue': Booking.objects.filter(status='confirmed').aggregate(t=Sum('total_price'))['t'] or 0,
    }
    recent_bookings = Booking.objects.filter(status='confirmed').select_related(
        'passenger', 'trip__route__origin', 'trip__route__destination', 'trip__agency'
    ).order_by('-booked_at')[:10]
    pending_agencies = Agency.objects.filter(status='pending').select_related('manager').order_by('created_at')

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_bookings': recent_bookings,
        'pending_agencies': pending_agencies,
    })


@admin_required
def admin_agencies(request):
    from apps.agency.models import Agency
    agencies = Agency.objects.select_related('manager').order_by('-created_at')
    return render(request, 'admin_panel/agencies.html', {'agencies': agencies})


@admin_required
def approve_agency(request, agency_id):
    from apps.agency.models import Agency
    agency = get_object_or_404(Agency, id=agency_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            agency.status = 'approved'
            agency.approved_at = timezone.now()
            agency.save()
            messages.success(request, f'{agency.name} approved.')
        elif action == 'suspend':
            agency.status = 'suspended'
            agency.save()
            messages.warning(request, f'{agency.name} suspended.')
    return redirect('dashboard:agencies')


@admin_required
def admin_users(request):
    from apps.accounts.models import User
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})
