from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Booking, Payment, Ticket
from .utils import confirm_booking
from apps.trips.models import Trip, Seat


@login_required
def booking_confirm(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, status='scheduled')

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seats')

        if not seat_ids:
            messages.error(request, 'Please select at least one seat.')
            return redirect('trip_detail', pk=trip_id)

        seats = Seat.objects.filter(id__in=seat_ids, trip=trip, is_booked=False)

        if seats.count() != len(seat_ids):
            messages.error(request, 'One or more selected seats are no longer available.')
            return redirect('trip_detail', pk=trip_id)

        request.session['pending_seats'] = seat_ids
        request.session['pending_trip'] = str(trip_id)

        total_price = trip.base_price * len(seat_ids)

        return render(request, 'passenger/booking_confirm.html', {
            'trip': trip,
            'seats': seats,
            'total_price': total_price,
            'seat_count': len(seat_ids),
        })

    return redirect('trip_detail', pk=trip_id)


@login_required
def create_booking(request):
    if request.method != 'POST':
        return redirect('home')

    seat_ids = request.session.get('pending_seats', [])
    trip_id = request.session.get('pending_trip')

    if not seat_ids or not trip_id:
        messages.error(request, 'Session expired. Please select seats again.')
        return redirect('home')

    trip = get_object_or_404(Trip, pk=trip_id, status='scheduled')
    seats = Seat.objects.filter(id__in=seat_ids, trip=trip, is_booked=False)

    if seats.count() != len(seat_ids):
        messages.error(request, 'Some seats were booked by another user. Please try again.')
        del request.session['pending_seats']
        del request.session['pending_trip']
        return redirect('trip_detail', pk=trip_id)

    total_price = trip.base_price * seats.count()
    booking = Booking.objects.create(
        passenger=request.user,
        trip=trip,
        total_price=total_price,
        status='pending',
    )
    booking.seats.set(seats)

    Payment.objects.create(booking=booking, amount=total_price)

    del request.session['pending_seats']
    del request.session['pending_trip']

    return redirect('payment', booking_id=booking.id)


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user, status='pending')

    if request.method == 'POST':
        method = request.POST.get('method', 'card')
        payment = booking.payment
        payment.method = method
        payment.status = 'successful'
        payment.transaction_id = f"TMS-TXN-{booking.booking_number}"
        payment.paid_at = timezone.now()
        payment.save()

        ticket = confirm_booking(booking)
        messages.success(request, 'Payment successful! Your ticket is ready.')
        return redirect('ticket_view', ticket_number=ticket.ticket_number)

    return render(request, 'passenger/payment.html', {'booking': booking})


@login_required
def ticket_view(request, ticket_number):
    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'booking__passenger',
            'booking__trip__route__origin',
            'booking__trip__route__destination',
            'booking__trip__bus',
            'booking__trip__driver',
            'booking__trip__agency',
        ),
        ticket_number=ticket_number,
        booking__passenger=request.user,
    )
    return render(request, 'passenger/ticket.html', {'ticket': ticket})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        passenger=request.user
    ).select_related(
        'trip__route__origin',
        'trip__route__destination',
        'trip__agency',
    ).prefetch_related('seats').order_by('-booked_at')
    return render(request, 'passenger/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)

    if booking.status not in ('pending', 'confirmed'):
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('my_bookings')

    if request.method == 'POST':
        booking.seats.all().update(is_booked=False)
        booking.status = 'cancelled'
        booking.cancellation_reason = request.POST.get('reason', 'Cancelled by passenger')
        booking.save()
        messages.success(request, f'Booking {booking.booking_number} cancelled.')
    return redirect('my_bookings')
