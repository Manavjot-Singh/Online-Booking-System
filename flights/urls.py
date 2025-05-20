from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,            name='home'),    
    path('search/', views.search,   name='search'),  
    path('book/<int:flight_id>/', views.book_flight, name='book'),
    path('lookup/', views.booking_lookup, name='booking_lookup'),
    path('cancel/', views.cancel_booking, name='cancel_booking'),
    path('about/', views.about, name='about'),

]
