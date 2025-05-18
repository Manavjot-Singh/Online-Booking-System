from django.contrib import admin
from .models import Aircraft, FlightSchedule, Flight, Passenger

admin.site.register(Aircraft)
admin.site.register(FlightSchedule)
admin.site.register(Flight)
admin.site.register(Passenger)
