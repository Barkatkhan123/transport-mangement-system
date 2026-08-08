import uuid
from django.db import models
from apps.agency.models import Agency, Driver, Bus


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departing_routes')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arriving_routes')
    distance_km = models.PositiveIntegerField(null=True, blank=True)
    estimated_duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} → {self.destination}"

    @property
    def duration_display(self):
        if not self.estimated_duration_minutes:
            return 'N/A'
        h = self.estimated_duration_minutes // 60
        m = self.estimated_duration_minutes % 60
        if h > 0 and m > 0:
            return f"{h}h {m}m"
        elif h > 0:
            return f"{h}h"
        elif m > 0:
            return f"{m}m"
        return '0m'

    @property
    def duration_hours(self):
        if not self.estimated_duration_minutes:
            return None
        hours = self.estimated_duration_minutes / 60
        return int(hours) if hours.is_integer() else round(hours, 2)


class Trip(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('boarding', 'Boarding'),
        ('departed', 'Departed'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='trips')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_datetime']

    def __str__(self):
        return f"{self.route} | {self.departure_datetime.strftime('%d %b %Y %H:%M')}"

    @property
    def duration_display(self):
        if self.departure_datetime and self.arrival_datetime:
            diff = self.arrival_datetime - self.departure_datetime
            total_seconds = int(diff.total_seconds())
            if total_seconds > 0:
                total_minutes = total_seconds // 60
                h = total_minutes // 60
                m = total_minutes % 60
                if h > 0 and m > 0:
                    return f"{h}h {m}m"
                elif h > 0:
                    return f"{h}h"
                elif m > 0:
                    return f"{m}m"
        return self.route.duration_display if self.route else 'N/A'

    @property
    def available_seats_count(self):
        return self.seats.filter(is_booked=False).count()

    @property
    def total_seats_count(self):
        return self.seats.count()

    @property
    def occupancy_percent(self):
        total = self.total_seats_count
        if total == 0:
            return 0
        booked = total - self.available_seats_count
        return int((booked / total) * 100)

    def get_status_color(self):
        colors = {
            'scheduled': 'blue',
            'boarding': 'yellow',
            'departed': 'purple',
            'arrived': 'green',
            'cancelled': 'red',
        }
        return colors.get(self.status, 'gray')


class Seat(models.Model):
    SEAT_TYPE_CHOICES = [('window', 'Window'), ('aisle', 'Aisle'), ('middle', 'Middle')]
    GENDER_CHOICES = [('any', 'Any'), ('male', 'Male Only'), ('female', 'Female Only')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    row_number = models.PositiveIntegerField()
    column_number = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES, default='window')
    is_booked = models.BooleanField(default=False)
    gender_restriction = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')

    class Meta:
        unique_together = ('trip', 'seat_number')
        ordering = ['row_number', 'column_number']

    def __str__(self):
        return f"Seat {self.seat_number} — {self.trip}"
