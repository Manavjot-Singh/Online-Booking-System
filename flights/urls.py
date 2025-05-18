from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,            name='home'),    # /
    path('search/', views.search,   name='search'),  # /search/
    path('book/<int:flight_id>/', views.book_flight, name='book'),    # /book/5/
]
