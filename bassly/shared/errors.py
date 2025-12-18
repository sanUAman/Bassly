from django.http import JsonResponse

def error_response(error: str, request_id: str, code=None, details=None, status=400):
    return JsonResponse(
        {
            "error": error,
            "code": code,
            "details": details,
            "requestId": request_id,
        },
        status=status,
    )