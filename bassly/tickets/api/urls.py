from django.urls import path
from .views import tickets_for_event, reserve_ticket

urlpatterns = [
    path("<int:eventId>", tickets_for_event),
    path("<int:ticketId>/reserve", reserve_ticket),
]
