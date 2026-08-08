import uuid
from django.db import models
from apps.accounts.models import User


class Agency(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manager = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency')
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='agency_logos/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Agencies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_approved(self):
        return self.status == 'approved'

    def get_status_color(self):
        colors = {
            'pending': 'yellow',
            'approved': 'green',
            'suspended': 'red',
        }
        return colors.get(self.status, 'gray')


class Driver(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='drivers')
    full_name = models.CharField(max_length=150)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='drivers/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.license_number})"

    def get_status_color(self):
        colors = {'active': 'green', 'on_leave': 'yellow', 'terminated': 'red'}
        return colors.get(self.status, 'gray')

    @property
    def total_trips_count(self):
        return self.trips.count()

    @property
    def completed_trips_count(self):
        return self.trips.filter(status='arrived').count()

    @property
    def upcoming_trips_count(self):
        return self.trips.filter(status='scheduled').count()


class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
        ('Sleeper', 'Sleeper'),
        ('Mini', 'Mini'),
    ]
    LAYOUT_CHOICES = [('2x2', '2x2'), ('2x3', '2x3')]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='buses')
    registration_number = models.CharField(max_length=50, unique=True)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES, default='AC')
    total_seats = models.PositiveIntegerField()
    seat_layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='2x2')
    model_name = models.CharField(max_length=100, blank=True)
    year_of_manufacture = models.PositiveIntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to='buses/', blank=True, null=True)
    amenities = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Buses'
        ordering = ['registration_number']

    def __str__(self):
        return f"{self.registration_number} — {self.bus_type} ({self.total_seats} seats)"

    def get_status_color(self):
        colors = {'active': 'green', 'maintenance': 'yellow', 'retired': 'red'}
        return colors.get(self.status, 'gray')

    def get_amenity_icons(self):
        icons = {
            'wifi': ('WiFi', 'M8.288 15.038a5.25 5.25 0 0 1 7.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 0 1 1.06 0Z'),
            'charging': ('Charging', 'M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z'),
            'tv': ('TV', 'M6 20.25h12m-7.5-3v3m3-3v3m-10.125-3h17.25c.621 0 1.125-.504 1.125-1.125V4.875c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125z'),
            'toilet': ('Toilet', 'M12 6v6m0 0v6m0-6h6m-6 0H6'),
        }
        result = []
        for key, (label, path) in icons.items():
            if self.amenities.get(key):
                result.append({'label': label, 'path': path})
        return result

    @property
    def total_revenue(self):
        from apps.bookings.models import Booking
        from django.db.models import Sum
        return Booking.objects.filter(trip__bus=self, status='confirmed').aggregate(t=Sum('total_price'))['t'] or 0

    @property
    def total_trips_count(self):
        return self.trips.count()

    @property
    def total_bookings_count(self):
        from apps.bookings.models import Booking
        return Booking.objects.filter(trip__bus=self, status='confirmed').count()
