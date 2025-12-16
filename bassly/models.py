from bassly.accounts.domain import User
from bassly.events.domain import Event
from bassly.tickets.domain import Ticket
from bassly.orders.domain import Order
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name