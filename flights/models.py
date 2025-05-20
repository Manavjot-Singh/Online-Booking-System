from decimal import Decimal
from django.db import models

class Aircraft(models.Model):
    code = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    serial_number = models.CharField(max_length=20, unique=True)
    manufacturer = models.CharField(max_length=50)
    
class FlightSchedule(models.Model):
    origin = models.CharField(max_length=4)
    destination = models.CharField(max_length=4)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    weekday = models.IntegerField(choices=[(i,i) for i in range(7)])
    dep_time = models.TimeField()
    arr_time = models.TimeField()
    flight_number = models.CharField(max_length=10, unique=True)
    tz_offset = models.DecimalField(max_digits=4, decimal_places=2)
    price         = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Base fare per seat in NZD"
    )
    
class Flight(models.Model):
    schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
    date = models.DateField()
    seats_available = models.PositiveIntegerField()
    
class Passenger(models.Model):
    instance = models.ForeignKey(Flight, on_delete=models.CASCADE)
    cust_first_name = models.CharField(max_length=50)
    cust_last_name = models.CharField(max_length=50)
    cust_email = models.EmailField(blank=True, null=True)
    cust_id = models.CharField(max_length=20, unique=True)
    booking_status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')], default='booked')
    booking_price   = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total price paid for this booking"
    )