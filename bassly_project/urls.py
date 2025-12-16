from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bassly.urls')),
    path("api/accounts/", include("bassly.accounts.api.urls")),
    path("api/events/", include("bassly.events.api.urls")),
    path("api/tickets/", include("bassly.tickets.api.urls")),
    path("api/orders/", include("bassly.orders.api.urls")),
    path("health", health),
]
