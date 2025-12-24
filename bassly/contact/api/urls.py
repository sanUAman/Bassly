from django.urls import path
from .views import send_message, contact_page

urlpatterns = [
    path("", contact_page, name="contact"),
    path("send/", send_message, name="send"),
]