from django.contrib import admin
from unfold.admin import ModelAdmin
from bassly.events.domain import Event
from bassly.tickets.domain import Ticket
from bassly.orders.domain import Order
from bassly.accounts.domain import User
from bassly.contact.domain import ContactUsMessage


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('id', 'title', 'artist', 'date', 'location', 'organizer', 'total_tickets', 'sold_tickets')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'artist', 'location')
    list_filter = ('date',)
    fields = ('title', 'artist', 'date', 'location', 'organizer', 'total_tickets', 'sold_tickets')


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ('id', 'event', 'owner', 'seat_number', 'status')
    list_display_links = ('id', 'event')
    list_filter = ('status',)
    search_fields = ('event__title', 'seat_number')
    readonly_fields = ('qr_code',)
    fields = ('event', 'owner', 'seat_number', 'status', 'qr_code')


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'ticket', 'user', 'status', 'created_at')
    list_display_links = ('id', 'ticket')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    fields = ('ticket', 'user', 'status', 'created_at')


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')
    list_display_links = ('id', 'username')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    fields = ('username', 'email', 'password', 'role')


@admin.register(ContactUsMessage)
class ContactUsMessageAdmin(ModelAdmin):
    list_display = ('id', 'get_user_display', 'subject', 'created_at')
    list_display_links = ('id', 'subject')
    search_fields = ('subject', 'user__username')
    readonly_fields = ('created_at',)
    fields = ('user', 'subject', 'message', 'created_at')

    @admin.display(description='User')
    def get_user_display(self, obj):
        return obj.user.username if obj.user else 'Guest'
