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

    message = request.POST.get("message")
    subject = request.POST.get("subject")
    user_id = request.session.get("user_id")

    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None

    ContactUsMessage.objects.create(
        user=user,
        message=message,
        subject=subject
    )

    return redirect("contact")
