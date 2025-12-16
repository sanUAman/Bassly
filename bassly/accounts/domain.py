from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin')
    )

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def is_admin(self):
        return self.role == 'admin'

    def is_organizer(self):
        return self.role == 'organizer'

    def __str__(self):
        return self.username