from django.urls import path
from .views import events_list, create_event, event_details

urlpatterns = [
    path("", events_list),
    path("create", create_event),
    path("<int:id>", event_details),
]