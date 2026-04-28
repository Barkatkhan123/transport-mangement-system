from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trip, Seat


@receiver(post_save, sender=Trip)
def create_seats_for_trip(sender, instance, created, **kwargs):
    if created:
        bus = instance.bus
        layout = bus.seat_layout
        total = bus.total_seats
        cols_per_side = 2 if layout == '2x2' else 3
        aisle_after = 2

        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        seats_to_create = []
        for i in range(total):
            row = i // (cols_per_side * 2) + 1
            col = i % (cols_per_side * 2) + 1
            seat_number = f"{letters[row - 1]}{col}"

            if col == 1 or col == cols_per_side * 2:
                seat_type = 'window'
            elif col == aisle_after or col == aisle_after + 1:
                seat_type = 'aisle'
            else:
                seat_type = 'middle'

            seats_to_create.append(Seat(
                trip=instance,
                seat_number=seat_number,
                row_number=row,
                column_number=col,
                seat_type=seat_type,
            ))
        Seat.objects.bulk_create(seats_to_create)
