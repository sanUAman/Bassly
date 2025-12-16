from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bassly.tickets import service


def serialize_ticket(ticket):
    return {
        "id": ticket.id,
        "eventId": ticket.event_id,
        "seat_number": ticket.seat_number,
        "status": ticket.status,
    }


def tickets_for_event(request, eventId):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    tickets = service.get_tickets_for_event(eventId)
    data = [serialize_ticket(t) for t in tickets]
    return JsonResponse(data, safe=False, status=200)


@csrf_exempt
def reserve_ticket(request, ticketId):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    ticket, error = service.reserve_ticket(ticketId)
    if error:
        return JsonResponse({"error": error}, status=400)

    return JsonResponse({"status": "reserved"}, status=200)
