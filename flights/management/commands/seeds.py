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
        # origin, destination, aircraft, weekday, dep_time, arr_time, flight_number, tz_offset   
        schedules = [
            ("NZNE", "YMML" , "SJ-001", 4 , "10:00", "12:00" , "SJ30i-001", 10.0),
            ("YMML", "NZNE" , "SJ-001", 6 , "14:00", "20:00" , "SJ30i-002", 12.0),
            ("NZME", "NZCI", "E-001", 1 ,"12:00" , "12:45" , "E001-001", 12.45),
            ("NZCI", "NZME", "E-001", 2 ,"13:00" , "15:15" , "E001-002", 12.0),
            ("NZME", "NZCI", "E-001", 4 ,"12:00" , "12:45" , "E001-003", 12.45),
            ("NZCI", "NZME", "E-001", 5 ,"13:00" , "15:15" , "E001-004", 12.0),
            ("NZNE", "NZTL", "E-002", 0 ,"14:00" , "15:30" , "E002-001", 12.0),
            ("NZTL", "NZNE", "E-002", 1 ,"15:00" , "16:30" , "E002-002", 12.0),
        ]
        for i in range(5):
            schedules.extend([
                ("NZNE", "NZRO" , "SF-001", i , "06:00", "07:00" , f"SF501-AM-{i}", 12.0),
                ("NZRO", "NZNE" , "SF-001", i , "08:00", "09:00" , f"SF501-AR-{i}", 12.0),
                ("NZNE", "NZRO" , "SF-001", i , "16:30", "17:30" , f"SF501-PM-{i}", 12.0),
                ("NZRO", "NZNE" , "SF-001", i , "18:30", "19:30" , f"SF501-PR-{i}", 12.0),
            ])
        for i in range(0,6,2):
            schedules.extend([
                ("NZNE", "NZGB", "SF-002", i , "09:00", "09:45", f"SF502-OB-{i}", 12.0),
                ("NZGB", "NZNE", "SF-002", i+1 , "09:00", "09:45", f"SF502-IB-{i+1}", 12.0),                    
            ])
        
        for origin, destination, aircraft, weekday, dep_time, arr_time, flight_number, tz_offset in schedules:
            aircraft = Aircraft.objects.get(serial_number=aircraft)
            fs, created = FlightSchedule.objects.get_or_create(
                origin=origin,
                destination=destination,
                aircraft=aircraft,
                weekday=weekday,
                dep_time=dep_time,
                arr_time=arr_time,
                flight_number=flight_number,
                tz_offset=tz_offset
            )
            
            today = datetime.date.today() 
            for j in range(28):
                d = today + datetime.timedelta(days=j)
                if d.weekday() == weekday:
                    Flight.objects.get_or_create(
                        schedule = fs,
                        date = d,
                        defaults={
                            'seats_available': aircraft.capacity
                        }
                    )
            self.stdout.write("Seeding Complete")
            
                   
                
            
        

        