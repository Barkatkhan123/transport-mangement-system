from django.contrib import admin
from .models import Booking, Payment, Ticket


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('transaction_id', 'status', 'paid_at')


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ('ticket_number', 'is_used', 'issued_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'passenger', 'trip', 'total_price', 'status', 'booked_at')
    list_filter = ('status', 'booked_at')
    search_fields = ('booking_number', 'passenger__email', 'passenger__full_name')
    inlines = [PaymentInline, TicketInline]
    readonly_fields = ('booking_number',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status', 'paid_at')
    list_filter = ('status', 'method')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'booking', 'is_used', 'issued_at')
    list_filter = ('is_used',)
    search_fields = ('ticket_number', 'booking__booking_number')
