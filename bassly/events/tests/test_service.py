from django.test import TestCase
from bassly.events import service
from bassly.accounts.domain import User
from bassly.events.domain import Event
from django.utils import timezone

class EventServiceSuccessTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="Test User",
            password="123456",
            email="test@example.com",
            role="Test_role"
        )

    def test_create_event_success(self):
        payload = {
            "title": "Rock Concert",
            "artist": "Imagine Dragons",
            "date": timezone.now().isoformat(),
            "location": "Kyiv",
            "organizer_id": self.user.id,
            "total_tickets": 100
        }

        is_valid, error = service.validate_event_payload(payload)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

        event = service.create_event(payload)

        self.assertIsInstance(event, Event)
        self.assertEqual(event.title, "Rock Concert")
        self.assertEqual(event.total_tickets, 100)
        self.assertEqual(event.sold_tickets, 0)


class EventServiceFailureTest(TestCase):

    def test_create_event_missing_field(self):
        payload = {
            # "title" відсутній
            "artist": "Imagine Dragons",
            "date": timezone.now().isoformat(),
            "location": "Kyiv",
            "organizer_id": 1,
            "total_tickets": 100
        }

        is_valid, error = service.validate_event_payload(payload)

        self.assertFalse(is_valid)
        self.assertIn("Missing fields", error)
