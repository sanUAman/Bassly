from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from bassly.accounts import service


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

    # поки без сесій — просто редірект
    return redirect("/")


@csrf_exempt
def signin_view(request):
    if request.method == "GET":
        return render(request, "accounts/signin.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(
            request,
            "accounts/signin.html",
            {"error": "Username and password are required"},
        )

    user = service.authenticate_user(username, password)

    if not user:
        return render(
            request,
            "accounts/signin.html",
            {"error": "Invalid credentials"},
        )

    return redirect("/")
