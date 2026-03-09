from django.shortcuts import render
from django.utils import timezone
from bassly.events.domain import Event, UserFeaturedEvent

def index(request):
    user = None
    user_featured_ids = []

    if request.session.get("user_id"):
        user = {
            "username": request.session.get("username"),
            "role": request.session.get("role"),
        }
        # Get user's featured event IDs
        user_featured_ids = list(
            UserFeaturedEvent.objects.filter(
                user_id=request.session.get("user_id")
            ).values_list('event_id', flat=True)
        )

    filter_type = request.GET.get('filter', 'all')
    now = timezone.now()
    
    if filter_type == 'today':
        events = Event.objects.filter(date__date=now.date()).order_by('date')
    elif filter_type == 'tomorrow':
        tomorrow = now.date() + timezone.timedelta(days=1)
        events = Event.objects.filter(date__date=tomorrow).order_by('date')
    elif filter_type == 'weekend':
        from datetime import timedelta
        days_until_saturday = (5 - now.weekday()) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        saturday = now.date() + timedelta(days=days_until_saturday)
        sunday = saturday + timedelta(days=1)
        events = Event.objects.filter(date__date__gte=saturday, date__date__lte=sunday).order_by('date')
    else:
        events = Event.objects.all().order_by('-date')[:8]

    return render(request, "bassly.html", {
        "user": user,
        "events": events,
        "user_featured_ids": user_featured_ids,
    })

def how_it_works(request):
    return render(request, "how_it_works.html")

def become_partner(request):
    return render(request, "become_partner.html")