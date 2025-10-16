from django.http import JsonResponse
from .models import Place

def get_places(request):
    places = list(Place.objects.values('id', 'name'))
    return JsonResponse({'places': places})

def index(request):
    from django.shortcuts import render
    return render(request, 'bassly.html')