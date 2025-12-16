from django.db import models
from bassly.events.domain import Event
from bassly.accounts.domain import User
import uuid


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("sold", "Sold"),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    seat_number = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def reserve(self, user=None):
        if self.status != "available":
            return False
        self.status = "reserved"
        self.owner = user
        self.save()
        return True

    def mark_as_sold(self):
        if self.status != "reserved":
            return False
        self.status = "sold"
        self.save()
        return True

    def __str__(self):
        return f"Ticket #{self.id} for {self.event.title}"
