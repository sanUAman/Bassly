from django.db import models
from bassly.accounts.domain import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_tickets = models.IntegerField(default=0)
    sold_tickets = models.IntegerField(default=0)

    def remaining_tickets(self):
        return self.total_tickets - self.sold_tickets

    def sell_ticket(self):
        if self.remaining_tickets() > 0:
            self.sold_tickets += 1
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.title} ({self.location})"
