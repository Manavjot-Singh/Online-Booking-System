from django.core.management.base import BaseCommand
from flights.models import Aircraft, FlightSchedule, Flight, Passenger
import datetime

class Command(BaseCommand):
    help = 'Seed aircraft, flight schedules, flights'
    
    def handle(self, *args, **opts):
        
        # Create Aircraft
        aircraft = Aircraft.objects.create(
            code='SJ30i',
            capacity=6,
            serial_number='Prestige-1',
            manufacturer='Syberjet')
        