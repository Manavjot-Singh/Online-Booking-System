from django.db import models

# Create your models here.
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
    
class Flight(models.Model):
    schedule = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE)
    date = models.DateField()
    seats_available = models.PositiveIntegerField()
    
class Passenger(models.Model):
    instance = models.ForeignKey(Flight, on_delete=models.CASCADE)
    cust_first_name = models.CharField(max_length=50)
    cust_last_name = models.CharField(max_length=50)
    cust_id = models.CharField(max_length=20, unique=True)
    booking_status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')], default='booked')