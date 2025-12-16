import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bassly.orders import service
from bassly.accounts.domain import User


def serialize_order(order):
    return {
        "id": order.id,
        "ticketId": order.ticket_id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
    }


@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    ticket_id = payload.get("ticketId")
    if not ticket_id:
        return JsonResponse({"error": "ticketId is required"}, status=400)

    # Тимчасово — без auth, беремо будь-якого користувача
    user = User.objects.first()
    if not user:
        return JsonResponse({"error": "No users found"}, status=400)

    order, error = service.create_order(ticket_id, user)
    if error:
        return JsonResponse({"error": error}, status=400)

    return JsonResponse(serialize_order(order), status=201)


@csrf_exempt
def pay_order(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    order, error = service.pay_order(id)
    if error:
        return JsonResponse({"error": error}, status=400)

    return JsonResponse({"status": "paid"}, status=200)
