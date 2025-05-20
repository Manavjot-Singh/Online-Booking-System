from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import uuid

from .models import Flight, Passenger
from .forms import BookingForm, BookingLookupForm, EmailLookupForm

TZ_OFFSETS = {
    'NZNE': 12.0,  
    'NZRO': 12.0,  
    'NZGB': 12.0, 
    'NZTL': 12.0,  
    'NZCI': 12.75, 
    'YMML': 10.0,  
}

def home(request):
    lookup_form   = BookingLookupForm(request.POST or None)
    lookup_result = None
    lookup_error  = None

    if request.method == 'POST' and lookup_form.is_valid():
        ref = lookup_form.cleaned_data['reference'].upper().strip()
        try:
            p = Passenger.objects.get(cust_id=ref)
            f = p.instance
            lookup_result = {
                'reference':   p.cust_id,
                'name':        f"{p.cust_first_name} {p.cust_last_name}",
                'status':      p.booking_status,
                'flight_no':   f.schedule.flight_number,
                'date':        f.date,
                'origin':      f.schedule.origin,
                'destination': f.schedule.destination,
                'dep_time':    f.schedule.dep_time,
                'arr_time':    f.schedule.arr_time,
            }
        except Passenger.DoesNotExist:
            lookup_error = "No booking found with that reference."

    return render(request, 'homepage.html', {
        'lookup_form':   lookup_form,
        'lookup_result': lookup_result,
        'lookup_error':  lookup_error,
    })

def search(request):
    origin      = request.GET.get('origin', '').upper()
    destination = request.GET.get('destination', '').upper()
    date_str    = request.GET.get('date', '')
    flights     = None

    if origin and destination and date_str:
       
        selected_date = timezone.datetime.fromisoformat(date_str).date()
     
        qs = Flight.objects.filter(
            schedule__origin=origin,
            schedule__destination=destination,
            date=selected_date
        )
        today = timezone.localdate()
        if selected_date == today:
            now_time = timezone.localtime().time()
            qs = qs.filter(schedule__dep_time__gte=now_time)

        flights = []
        for f in qs:
        
            orig_off = float(f.schedule.tz_offset)
            dest_off = TZ_OFFSETS.get(f.schedule.destination, orig_off)
            dep_naive = datetime.combine(f.date, f.schedule.dep_time)
            arr_naive = datetime.combine(f.date, f.schedule.arr_time)
            dep_local = dep_naive
            arr_utc   = arr_naive - timedelta(hours=orig_off)
            arr_local = arr_utc  + timedelta(hours=dest_off)
            flights.append({
                'flight': f,
                'seats_left': f.seats_available,
                'dep_time':    dep_local.time(),
                'arr_time':    arr_local.time(),
            })
 
    return render(request, 'search.html', {
        'origin':      origin,
        'destination': destination,
        'date':        date_str,
        'flights':     flights
    })

def book_flight(request, flight_id):
    
    flight = get_object_or_404(Flight, pk=flight_id)
    dep_dt = datetime.combine(flight.date, flight.schedule.dep_time)
    dep_dt = timezone.make_aware(dep_dt)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            price_per_seat = flight.schedule.price
            total_price    = price_per_seat
            
            if dep_dt < timezone.now():
                messages.error(request, "You can’t book a flight that has already departed.")
                return redirect('search')
            
            if flight.seats_available < 1:
                form.add_error(None, 'No seats left on this flight.')
            else:
                ref = uuid.uuid4().hex[:20].upper()
                Passenger.objects.create(
                    instance=flight,
                    cust_first_name=form.cleaned_data['first_name'],
                    cust_last_name=form.cleaned_data['last_name'],
                    cust_id=ref,
                    cust_email=form.cleaned_data['email'],
                    booking_status='booked',
                    booking_price=total_price,
                )

                flight.seats_available -= 1
                flight.save()

                return render(request, 'bookings.html', {
                    'booked': True,
                    'reference': ref,
                    'total_price': total_price,
                })

    else:
        form = BookingForm()

    return render(request, 'bookings.html', {
        'flight': flight,
        'form':   form,
        'booked': False
    })

def booking_lookup(request):
    ref_form   = BookingLookupForm(request.POST or None)
    email_form = EmailLookupForm(request.POST or None)

    lookup_result  = None
    lookup_error   = None
    email_results  = None

    if request.method == 'POST':
        
        if 'reference' in request.POST and ref_form.is_valid():
            ref = ref_form.cleaned_data['reference'].upper().strip()
            try:
                p = Passenger.objects.get(cust_id=ref)
                f = p.instance
                lookup_result = {
                    'reference': ref,
                    'name':      f"{p.cust_first_name} {p.cust_last_name}",
                    'status':    p.booking_status,
                    'flight_no': f.schedule.flight_number,
                    'date':      f.date,
                    'origin':    f.schedule.origin,
                    'destination': f.schedule.destination,
                    'dep_time':  f.schedule.dep_time,
                    'arr_time':  f.schedule.arr_time,
                }
            except Passenger.DoesNotExist:
                lookup_error = "No booking found with that reference."
        
        elif 'email' in request.POST and email_form.is_valid():
            em = email_form.cleaned_data['email'].lower().strip()
            qs = Passenger.objects.filter(
                cust_email__iexact=em
            ).select_related('instance__schedule').order_by('-instance__date')
            email_results = []
            for p in qs:
                f = p.instance
                email_results.append({
                    'reference': p.cust_id,
                    'date':      f.date,
                    'flight_no': f.schedule.flight_number,
                    'route':     f"{f.schedule.origin} → {f.schedule.destination}",
                    'status':    p.booking_status,
                })

    return render(request, 'details.html', {
        'lookup_form':   ref_form,
        'email_form':    email_form,
        'lookup_result': lookup_result,
        'lookup_error':  lookup_error,
        'email_results': email_results,
    })
    
def cancel_booking(request):
    if request.method == 'POST':
        ref = request.POST.get('reference', '').upper().strip()
        
        try:
            passenger = Passenger.objects.get(cust_id=ref)
            if passenger.booking_status != 'cancelled':
                passenger.booking_status = 'cancelled'
                passenger.save()

                flight = passenger.instance
                flight.seats_available += 1
                flight.save()
           
                return render(request, 'details.html', {
                    'lookup_form': BookingLookupForm(),
                    'email_form': EmailLookupForm(),
                    'lookup_result': None,
                    'lookup_error': None,
                    'email_results': None,
                    'cancel_success': f"Booking {ref} has been cancelled."
                })
            else:
                return render(request, 'details.html', {
                    'lookup_form': BookingLookupForm(),
                    'lookup_result': None,
                    'lookup_error': f"Booking {ref} was already cancelled."
                })
        except Passenger.DoesNotExist:
            return render(request, 'details.html', {
                'lookup_form': BookingLookupForm(),
                'lookup_result': None,
                'lookup_error': "Booking not found."
            })

    return HttpResponseRedirect(reverse('booking_lookup'))    

def about(request):
    return render(request, 'about.html')