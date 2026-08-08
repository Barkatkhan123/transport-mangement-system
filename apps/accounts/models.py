import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agency', 'Agency Manager'),
        ('passenger', 'Passenger'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passenger')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def is_agency_manager(self):
        return self.role == 'agency'

    @property
    def is_passenger(self):
        return self.role == 'passenger'

    @property
    def is_admin_user(self):
        return self.role == 'admin'

    def get_initials(self):
        parts = self.full_name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return self.full_name[0].upper() if self.full_name else 'U'

    @property
    def total_travels_count(self):
        return self.bookings.filter(status='confirmed').count()

    @property
    def total_spent(self):
        from django.db.models import Sum
        return self.bookings.filter(status='confirmed').aggregate(t=Sum('total_price'))['t'] or 0

    def get_travel_history_breakdown(self):
        confirmed_bookings = self.bookings.filter(status='confirmed').select_related(
            'trip__agency', 'trip__route__origin', 'trip__route__destination'
        )
        grouped = {}
        for b in confirmed_bookings:
            agency_name = b.trip.agency.name
            origin_name = b.trip.route.origin.name
            dest_name = b.trip.route.destination.name
            key = (agency_name, origin_name, dest_name)
            if key not in grouped:
                grouped[key] = {
                    'agency_name': agency_name,
                    'origin': origin_name,
                    'destination': dest_name,
                    'trips_count': 0,
                    'total_spent': 0,
                    'last_traveled': b.booked_at,
                }
            grouped[key]['trips_count'] += 1
            grouped[key]['total_spent'] += float(b.total_price)
            if b.booked_at > grouped[key]['last_traveled']:
                grouped[key]['last_traveled'] = b.booked_at

        for record in grouped.values():
            cnt = record['trips_count']
            record['summary'] = f"{cnt} travel{'s' if cnt > 1 else ''} with {record['agency_name']} from {record['origin']} to {record['destination']}"

        return list(grouped.values())

    @property
    def travel_records_summary(self):
        records = self.get_travel_history_breakdown()
        if not records:
            return "No travel history yet"
        return ", ".join(r['summary'] for r in records)


class PassengerProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile: {self.user.full_name}"
