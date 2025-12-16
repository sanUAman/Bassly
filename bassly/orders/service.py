from django.shortcuts import get_object_or_404
from bassly.orders.domain import Order
from bassly.tickets.domain import Ticket


def create_order(ticket_id, user):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status != "reserved":
        return None, "Ticket must be reserved before ordering"

    order = Order.objects.create(
        ticket=ticket,
        user=user,
        status="created"
    )

    return order, None


def pay_order(order_id):
    order = get_object_or_404(Order, id=order_id)

    if not order.pay():
        return None, "Order cannot be paid"

    ticket = order.ticket
    ticket.mark_as_sold()

    return order, None
