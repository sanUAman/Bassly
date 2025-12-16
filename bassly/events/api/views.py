import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bassly.events import service


def serialize_event(event):
    return {
        "id": event.id,
        "title": event.title,
        "artist": event.artist,
        "date": event.date.isoformat(),
        "location": event.location,
        "total_tickets": event.total_tickets,
        "sold_tickets": event.sold_tickets,
    }


@csrf_exempt
def events_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    events = service.get_event_list()
    data = [serialize_event(e) for e in events]
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
