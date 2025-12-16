from bassly.events.domain import Event
from bassly.accounts.domain import User
from django.shortcuts import get_object_or_404
from datetime import datetime


def validate_event_payload(data):
    required_fields = [
        "title",
        "artist",
        "date",
        "location",
        "organizer_id",
        "total_tickets"
    ]

    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"

    try:
        datetime.fromisoformat(data["date"])
    except ValueError:
        return False, "Invalid date format. Expected ISO format."

    if int(data["total_tickets"]) < 0:
        return False, "total_tickets cannot be negative."

    return True, None


def create_event(data):
    organizer = get_object_or_404(User, id=data["organizer_id"])

    return Event.objects.create(
        title=data["title"],
        artist=data["artist"],
        date=data["date"],
        location=data["location"],
        organizer=organizer,
        total_tickets=data["total_tickets"],
        sold_tickets=0
    )


def get_event(event_id):
    return get_object_or_404(Event, id=event_id)


def get_event_list():
    return Event.objects.all()
