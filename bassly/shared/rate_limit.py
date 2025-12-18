import time
from collections import defaultdict
from django.http import JsonResponse

WINDOW = 10
MAX_REQ = 8
buckets = defaultdict(list)

def rate_limit_middleware(get_response):
    def middleware(request):
        ip = request.META.get("REMOTE_ADDR", "local")
        now = time.time()

        buckets[ip] = [t for t in buckets[ip] if now - t < WINDOW]
        buckets[ip].append(now)

        if len(buckets[ip]) > MAX_REQ:
            res = JsonResponse(
                {"error": "too_many_requests", "requestId": request.request_id},
                status=429,
            )
            res["Retry-After"] = "2"
            return res

        return get_response(request)

    return middleware
