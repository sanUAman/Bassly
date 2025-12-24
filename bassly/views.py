from django.shortcuts import render

def index(request):
    user = None

    if request.session.get("user_id"):
        user = {
            "username": request.session.get("username"),
            "role": request.session.get("role"),
        }

    return render(request, "bassly.html", {
        "user": user
    })

def how_it_works(request):
    return render(request, "how_it_works.html")