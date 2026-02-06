from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from bassly.contact.domain import ContactUsMessage
from bassly.accounts.domain import User


def contact_page(request):
    return render(request, "contact.html")


@csrf_exempt
def send_message(request):
    if request.method != "POST":
        return redirect("contact")

    user_id = request.session.get("user_id")
    if not user_id:
        return render(request, "contact.html", {"show_signin_modal": True})

    message = request.POST.get("message")
    subject = request.POST.get("subject")

    user = None
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, "contact.html", {"show_signin_modal": True})

    ContactUsMessage.objects.create(
        user=user,
        message=message,
        subject=subject
    )

    return redirect("contact")
