from bassly.tickets.domain import Ticket
from bassly.events.domain import Event
from django.shortcuts import get_object_or_404


def get_tickets_for_event(event_id):
    return Ticket.objects.filter(event_id=event_id)


def reserve_ticket(ticket_id, user=None):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status != "available":
        return None, "Ticket is not available"

    ticket.reserve(user)
    return ticket, None
