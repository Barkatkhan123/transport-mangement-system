import qrcode
import json
import io
from django.core.files.base import ContentFile
from django.utils import timezone


def generate_qr_code(ticket):
    booking = ticket.booking
    trip = booking.trip

    qr_data = {
        'ticket_number': str(ticket.ticket_number),
        'booking_number': booking.booking_number,
        'passenger': booking.passenger.full_name,
        'route': str(trip.route),
        'departure': trip.departure_datetime.strftime('%d %b %Y %H:%M'),
        'seats': booking.seat_numbers,
        'bus': trip.bus.registration_number,
    }
    qr_json = json.dumps(qr_data)
    ticket.qr_data = qr_json

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_json)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#1D4ED8', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"ticket_{ticket.ticket_number}.png"
    ticket.qr_code_image.save(filename, ContentFile(buffer.read()), save=False)
    ticket.save()
    return ticket


def confirm_booking(booking):
    from apps.bookings.models import Payment, Ticket

    booking.status = 'confirmed'
    booking.save()

    booking.seats.all().update(is_booked=True)

    ticket, created = Ticket.objects.get_or_create(booking=booking)
    if created:
        generate_qr_code(ticket)

    try:
        send_booking_email(booking)
    except Exception:
        pass

    return ticket


def send_booking_email(booking):
    from django.core.mail import send_mail
    from django.conf import settings

    trip = booking.trip
    subject = f"Booking Confirmed — {booking.booking_number}"
    message = f"""
Dear {booking.passenger.full_name},

Your booking has been confirmed!

Booking Number: {booking.booking_number}
Route: {trip.route}
Departure: {trip.departure_datetime.strftime('%d %b %Y at %H:%M')}
Seats: {booking.seat_numbers}
Total Paid: PKR {booking.total_price}

Please show your QR ticket at the boarding point.
Login to view your ticket: http://localhost:8000/bookings/

Safe travels!
TMS Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.passenger.email],
        fail_silently=True,
    )
