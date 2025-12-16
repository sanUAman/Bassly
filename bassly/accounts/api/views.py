import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bassly.accounts import service


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user, error = service.register_user(payload)
    if error:
        return JsonResponse({"error": error}, status=400)

    return JsonResponse(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        status=201
    )


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        return JsonResponse({"error": "email and password are required"}, status=400)

    user = service.authenticate_user(email, password)
    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        status=200
    )
