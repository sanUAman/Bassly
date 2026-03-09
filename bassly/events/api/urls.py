from django.urls import path
from .views import events_list, create_event, event_details, toggle_featured, featured_events

urlpatterns = [
    path("", events_list),
    path("create", create_event),
    path("<int:id>", event_details),
    path("<int:id>/featured", toggle_featured),
    path("featured", featured_events),
]