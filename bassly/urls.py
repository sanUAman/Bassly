from django.urls import path
from .views import index, how_it_works

urlpatterns = [
    path('', index),
    path("how-it-works/", how_it_works, name="how_it_works"),
]