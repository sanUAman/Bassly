from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', include('bassly.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("bassly.accounts.api.urls")),
    path("contact/", include("bassly.contact.api.urls")),
    path("health", health),
]
