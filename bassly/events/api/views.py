import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from bassly.events import service
from bassly.events.domain import Event


def get_user_id_from_session(request):
    """Get user ID from session, returns None if not logged in"""
    return request.session.get('user_id')


def serialize_event(event, is_featured=False):
    image_url = None
    if event.image:
        image_url = event.image.url
    return {
        "id": event.id,
        "title": event.title,
        "artist": event.artist,
        "date": event.date.isoformat(),
        "location": event.location,
        "total_tickets": event.total_tickets,
        "sold_tickets": event.sold_tickets,
        "is_featured": is_featured,
        "image": image_url,
    }


@csrf_exempt
def events_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    filter_type = request.GET.get('filter', 'all')
    
    now = timezone.now()
    
    if filter_type == 'today':
        events = Event.objects.filter(date__date=now.date()).order_by('date')
    elif filter_type == 'tomorrow':
        tomorrow = now.date() + timezone.timedelta(days=1)
        events = Event.objects.filter(date__date=tomorrow).order_by('date')
    elif filter_type == 'weekend':
        days_until_saturday = (5 - now.weekday()) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        saturday = now.date() + timedelta(days=days_until_saturday)
        sunday = saturday + timedelta(days=1)
        events = Event.objects.filter(date__date__gte=saturday, date__date__lte=sunday).order_by('date')
    else:
        events = Event.objects.all().order_by('-date')[:8]
    
    user_id = get_user_id_from_session(request)
    
    data = []
    for event in events:
        is_featured = False
        if user_id:
            is_featured = service.is_event_featured_for_user(user_id, event.id)
        data.append(serialize_event(event, is_featured))
    
    return JsonResponse(data, safe=False, status=200)


@csrf_exempt
def create_event(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    ok, error = service.validate_event_payload(payload)
    if not ok:
        return JsonResponse({"error": error}, status=400)

    event = service.create_event(payload)
    return JsonResponse(serialize_event(event), status=201)


@csrf_exempt
def event_details(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        event = service.get_event(id)
        return JsonResponse(serialize_event(event), status=200)
    except:
        return JsonResponse({"error": "Event not found"}, status=404)


@csrf_exempt
def toggle_featured(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user_id = get_user_id_from_session(request)
    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    try:
        event, is_featured = service.toggle_user_featured(user_id, id)
        return JsonResponse(serialize_event(event, is_featured), status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


@csrf_exempt
def featured_events(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user_id = get_user_id_from_session(request)
    if not user_id:
        return JsonResponse([], safe=False, status=200)

    events = service.get_user_featured_events(user_id)
    data = [serialize_event(e, True) for e in events]
    return JsonResponse(data, safe=False, status=200)
