import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.trips.models import City, Route, Trip, Seat
from apps.agency.models import Agency, Bus, Driver
from apps.accounts.models import User

def seed_data():
    # 1. Create cities
    khi, _ = City.objects.get_or_create(name="Karachi", defaults={"province": "Sindh"})
    lhr, _ = City.objects.get_or_create(name="Lahore", defaults={"province": "Punjab"})
    isl, _ = City.objects.get_or_create(name="Islamabad", defaults={"province": "ICT"})
    
    print("Cities created.")

    # 2. Create an Agency Manager if not exists
    manager, created = User.objects.get_or_create(
        email="agency@tms.com",
        defaults={
            "full_name": "Agency Manager",
            "role": "agency"
        }
    )
    if created:
        manager.set_password("pass123")
        manager.save()
    
    # 3. Create Agency
    agency, _ = Agency.objects.get_or_create(
        manager=manager,
        defaults={
            "name": "TMS Express",
            "registration_number": "TMS-001",
            "email": "contact@tmsexpress.com",
            "phone": "0300-1234567",
            "address": "Main Terminal, Karachi",
            "city": "Karachi",
            "status": "approved"
        }
    )
    print("Agency created.")

    # 4. Create Route
    route, _ = Route.objects.get_or_create(
        origin=khi,
        destination=lhr,
        defaults={"distance_km": 1200, "estimated_duration_minutes": 1080}
    )
    print("Route created.")

    # 5. Create Bus
    bus, _ = Bus.objects.get_or_create(
        agency=agency,
        registration_number="ABC-123",
        defaults={
            "bus_type": "AC",
            "total_seats": 40,
            "seat_layout": "2x2",
            "model_name": "Higer Super"
        }
    )
    print("Bus created.")

    # 6. Create Driver
    driver, _ = Driver.objects.get_or_create(
        agency=agency,
        license_number="LIC-12345",
        defaults={
            "full_name": "John Driver",
            "phone_number": "0311-1112223",
            "license_expiry_date": timezone.now().date() + timedelta(days=365)
        }
    )
    print("Driver created.")

    # 7. Create Trip
    departure = timezone.now() + timedelta(days=1)
    departure = departure.replace(hour=20, minute=0, second=0, microsecond=0)
    arrival = departure + timedelta(minutes=1080)
    
    trip, created = Trip.objects.get_or_create(
        agency=agency,
        route=route,
        departure_datetime=departure,
        defaults={
            "arrival_datetime": arrival,
            "bus": bus,
            "driver": driver,
            "base_price": 5500,
            "status": "scheduled"
        }
    )
    
    if created:
        # Create seats manually
        for r in range(1, 11):
            for c in range(1, 5):
                Seat.objects.get_or_create(
                    trip=trip, 
                    seat_number=f"{chr(64+r)}{c}", 
                    defaults={
                        "row_number": r, 
                        "column_number": c,
                        "seat_type": 'window' if c in [1, 4] else 'aisle'
                    }
                )
    else:
        # If trip already exists, ensure it has seats
        if not trip.seats.exists():
            for r in range(1, 11):
                for c in range(1, 5):
                    Seat.objects.create(
                        trip=trip, 
                        seat_number=f"{chr(64+r)}{c}", 
                        row_number=r, 
                        column_number=c,
                        seat_type='window' if c in [1, 4] else 'aisle'
                    )
    
    print("Trip and Seats created.")

if __name__ == "__main__":
    seed_data()
