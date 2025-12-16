from django.db import models
from bassly.tickets.domain import Ticket
from bassly.accounts.domain import User


class Order(models.Model):
    STATUS_CHOICES = (
        ("created", "Created"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def pay(self):
        if self.status != "created":
            return False

        self.status = "paid"
        self.save()
        return True

    def cancel(self):
        if self.status == "paid":
            return False

        self.status = "cancelled"
        self.save()
        return True

    def __str__(self):
        return f"Order #{self.id} ({self.status})"
