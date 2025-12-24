from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from bassly.accounts import service
from bassly.accounts.domain import User


@csrf_exempt
def signup_view(request):
    if request.method == "GET":
        return render(request, "accounts/signup.html")

    # POST
    payload = {
        "username": request.POST.get("username"),
        "email": request.POST.get("email"),
        "password": request.POST.get("password"),
        "role": request.POST.get("role", "user"),
    }

    user, error = service.register_user(payload)

    if error:
        return render(
            request,
            "accounts/signup.html",
            {"error": error},
        )

    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role
    
    return redirect("/")


@csrf_exempt
def signin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "accounts/signin.html", {
                "error": "Username and password are required"
            })

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "accounts/signin.html", {
                "error": "Invalid credentials"
            })

        if user.password != password:
            return render(request, "accounts/signin.html", {
                "error": "Invalid credentials"
            })

        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["role"] = user.role

        return redirect("/")

    return render(request, "accounts/signin.html")


def logout_view(request):
    request.session.flush()
    return redirect("/")