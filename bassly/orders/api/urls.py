from django.urls import path
from .views import create_order, pay_order

urlpatterns = [
    path("", create_order),
    path("<int:id>/pay", pay_order)
]
