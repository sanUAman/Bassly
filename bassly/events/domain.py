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
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

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


class UserFeaturedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='featured_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='featured_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
