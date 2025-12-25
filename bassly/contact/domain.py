from bassly.accounts.domain import User
from django.db import models

class ContactUsMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True, blank=True
    )
    message = models.TextField()
    subject = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message #{self.id} from {self.user}"