from decimal import Decimal
from django.core.management.base import BaseCommand
from flights.models import Aircraft, FlightSchedule, Flight, Passenger
import datetime

class Command(BaseCommand):
    help = 'Seed aircraft, flight schedules, flights'
    
    def handle(self, *args, **opts):
        planes = [
            ("SJ30i", 6 , "SJ-001", "Syberjet"),
            ("SF50" , 4 , "SF-001", "Cirrus"),
            ("SF50", 4 , "SF-002" , "Cirrus"),
            ("Elite", 5 , "E-001", "Hondajet"),
            ("Elite", 5 , "E-002", "Hondajet"),      
        ]
        
        for code, capacity, serial_number, manufacturer in planes:
            Aircraft.objects.get_or_create(
                code=code,
                capacity=capacity,
                serial_number=serial_number,
                manufacturer=manufacturer
            )
           
        schedules = [
            ("NZNE", "YMML" , "SJ-001", 4 , "10:00", "14:00" , "SJ30i-001", 12.0, Decimal('550.00')),
            ("YMML", "NZNE" , "SJ-001", 6 , "15:00", "18:40" , "SJ30i-002", 10.0, Decimal('550.00')),
            ("NZNE", "NZCI", "E-001", 1 ,"12:00" , "12:45" , "E001-001", 12.00, Decimal('350.00')),
            ("NZCI", "NZNE", "E-001", 2 ,"13:00" , "15:15" , "E001-002", 12.75, Decimal('350.00')),
            ("NZNE", "NZCI", "E-001", 4 ,"12:00" , "12:45" , "E001-003", 12.00, Decimal('350.00')),
            ("NZCI", "NZNE", "E-001", 5 ,"13:00" , "15:15" , "E001-004", 12.75, Decimal('350.00')),
            ("NZNE", "NZTL", "E-002", 0 ,"14:00" , "15:30" , "E002-001", 12.0, Decimal('300.00')),
            ("NZTL", "NZNE", "E-002", 1 ,"15:00" , "16:30" , "E002-002", 12.0, Decimal('300.00')),
        ]
        for i in range(5):
            schedules.extend([
                ("NZNE", "NZRO" , "SF-001", i , "06:00", "07:00" , f"SF501-AM-{i}", 12.0, Decimal('200.00')),
                ("NZRO", "NZNE" , "SF-001", i , "08:00", "09:00" , f"SF501-AR-{i}", 12.0, Decimal('200.00')),
                ("NZNE", "NZRO" , "SF-001", i , "16:30", "17:30" , f"SF501-PM-{i}", 12.0, Decimal('200.00')),
                ("NZRO", "NZNE" , "SF-001", i , "18:30", "19:30" , f"SF501-PR-{i}", 12.0, Decimal('200.00')),
            ])
        for i in range(0,6,2):
            schedules.extend([
                ("NZNE", "NZGB", "SF-002", i , "09:00", "09:45", f"SF502-OB-{i}", 12.0, Decimal('150.00')),
                ("NZGB", "NZNE", "SF-002", i+1 , "09:00", "09:45", f"SF502-IB-{i+1}", 12.0, Decimal('150.00')),                    
            ])
        
        for origin, dest, ac_serial, weekday, dep, arr, flight_no, tz_off, price in schedules:
            ac = Aircraft.objects.get(serial_number=ac_serial)

            
            fs, created = FlightSchedule.objects.update_or_create(
                flight_number=flight_no,
                defaults={
                    'origin':       origin,
                    'destination':  dest,
                    'aircraft':     ac,
                    'weekday':      weekday,
                    'dep_time':     dep,
                    'arr_time':     arr,
                    'tz_offset':    tz_off,
                    'price':        price,
                }
            )
            
            today = datetime.date.today() 
            for j in range(28):
                d = today + datetime.timedelta(days=j)
                if d.weekday() == weekday:
                    Flight.objects.get_or_create(
                        schedule = fs,
                        date = d,
                        defaults={
                            'seats_available': ac.capacity
                        }
                    )
            self.stdout.write("Seeding Complete")
            
                   
                
            
        

        