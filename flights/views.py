from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import uuid

from .models import Flight, Passenger
from .forms import BookingForm

def home(request):
   
    return render(request, 'homepage.html')


def search(request):
    origin      = request.GET.get('origin', '').upper()
    destination = request.GET.get('destination', '').upper()
    date_str    = request.GET.get('date', '')
    flights     = None

    if origin and destination and date_str:
       
        date = timezone.datetime.fromisoformat(date_str).date()

     
        qs = Flight.objects.filter(
            schedule__origin=origin,
            schedule__destination=destination,
            date=date
        )

        
        flights = qs 

    return render(request, 'search.html', {
        'origin':      origin,
        'destination': destination,
        'date':        date_str,
        'flights':     flights
    })


def book_flight(request, flight_id):
    
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            print("🔍 Form is valid")

            if flight.seats_available < 1:
                form.add_error(None, 'No seats left on this flight.')
            else:
                ref = uuid.uuid4().hex[:20].upper()

                Passenger.objects.create(
                    instance=flight,
                    cust_first_name=form.cleaned_data['first_name'],
                    cust_last_name=form.cleaned_data['last_name'],
                    cust_id=ref,
                    booking_status='booked'
                )

                flight.seats_available -= 1
                flight.save()

                return render(request, 'bookings.html', {
                    'booked': True,
                    'reference': ref
                })

    else:
        form = BookingForm()
        



    return render(request, 'bookings.html', {
        'flight': flight,
        'form':   form,
        'booked': False
    })
