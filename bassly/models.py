from django.db import models
from django.utils import timezone

class Place(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# User

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

# Event

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
    
# Ticket

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    seat_number = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def reserve(self, user):
        if self.status == 'available':
            self.status = 'reserved'
            self.owner = user
            self.save()
            return True
        return False

    def mark_as_sold(self):
        if self.status == 'reserved':
            self.status = 'sold'
            self.save()
            return True
        return False

    def __str__(self):
        return f"Ticket #{self.id} for {self.event.title}"
    
# Order

class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)

    def pay(self):
        if self.status == 'created':
            self.status = 'paid'
            self.ticket.mark_as_sold()
            self.save()
            return True
        return False

    def cancel(self):
        if self.status != 'paid':
            self.status = 'canceled'
            self.ticket.status = 'available'
            self.ticket.owner = None
            self.ticket.save()
            self.save()
            return True
        return False

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"