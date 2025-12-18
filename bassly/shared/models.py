from django.db import models

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
