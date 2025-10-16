from django.urls import path
from .views import get_places, index

urlpatterns = [
    path('places', get_places),
    path('', index),
]