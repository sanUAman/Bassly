import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bassly.orders import service
from bassly.accounts.domain import User
from bassly.shared.errors import error_response
from bassly.shared.models import IdempotencyKey


def serialize_order(order):
    return {
        "id": order.id,
        "ticketId": order.ticket_id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
    }


@csrf_exempt
def create_order(request):
    rid = getattr(request, "request_id", None)

    if request.method != "POST":
        return error_response("method_not_allowed", rid, status=405)

    idem_key = request.headers.get("Idempotency-Key")
    if not idem_key:
        return error_response("idempotency_key_required", rid, status=400)

    cached = IdempotencyKey.objects.filter(key=idem_key).first()
    if cached:
        data = cached.response
        data["requestId"] = rid
        return JsonResponse(data, status=201)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return error_response("invalid_json", rid, status=400)

    ticket_id = payload.get("ticketId")
    if not ticket_id:
        return error_response("ticket_id_required", rid, status=400)

    user = User.objects.first()
    if not user:
        return error_response("no_users_found", rid, status=400)

    order, error = service.create_order(ticket_id, user)
    if error:
        return error_response(error, rid, status=400)

    response_data = serialize_order(order)

    IdempotencyKey.objects.create(
        key=idem_key,
        response=response_data,
    )

    response_data["requestId"] = rid
    return JsonResponse(response_data, status=201)


@csrf_exempt
def pay_order(request, id):
    rid = getattr(request, "request_id", None)

    if request.method != "POST":
        return error_response("method_not_allowed", rid, status=405)

    order, error = service.pay_order(id)
    if error:
        return error_response(error, rid, status=400)

    return JsonResponse({"status": "paid", "requestId": rid}, status=200)

