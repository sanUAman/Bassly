from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from bassly.accounts import service
from bassly.accounts.domain import User


@csrf_exempt
def signup_view(request):
    user = None
    if request.session.get("user_id"):
        user = {
            "username": request.session.get("username"),
            "role": request.session.get("role"),
        }

    if request.method == "GET":
        return render(request, "bassly.html", {
            "user": user,
            "show_signup_modal": True
        })

    # POST
    payload = {
        "username": request.POST.get("username"),
        "email": request.POST.get("email"),
        "password": request.POST.get("password"),
        "role": request.POST.get("role", "user"),
    }

    user_obj, error = service.register_user(payload)

    if error:
        return render(
            request,
            "bassly.html",
            {
                "user": user,
                "error": error,
                "show_signup_modal": True
            },
        )

    request.session["user_id"] = user_obj.id
    request.session["username"] = user_obj.username
    request.session["role"] = user_obj.role
    
    return redirect("/")


@csrf_exempt
def signin_view(request):
    user = None
    if request.session.get("user_id"):
        user = {
            "username": request.session.get("username"),
            "role": request.session.get("role"),
        }

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "bassly.html", {
                "user": user,
                "signin_error": "Username and password are required",
                "show_signin_modal": True
            })

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "bassly.html", {
                "user": user,
                "signin_error": "Invalid credentials",
                "show_signin_modal": True
            })

        if user_obj.password != password:
            return render(request, "bassly.html", {
                "user": user,
                "signin_error": "Invalid credentials",
                "show_signin_modal": True
            })

        request.session["user_id"] = user_obj.id
        request.session["username"] = user_obj.username
        request.session["role"] = user_obj.role

        return redirect("/")

    return render(request, "bassly.html", {"user": user})


def logout_view(request):
    request.session.flush()
    return redirect("/")