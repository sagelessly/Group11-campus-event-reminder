"""
tests/test_event.py
Member 2 - Unit tests for the Event class.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from event import Event, InvalidEventDataError


class TestEvent(unittest.TestCase):

    def test_create_valid_event(self):
        event = Event("Hackathon", "2026-08-01", "09:00", "Main Hall", "Annual coding event")
        self.assertEqual(event.title, "Hackathon")
        self.assertEqual(event.date, "2026-08-01")

    def test_empty_title_raises_error(self):
        with self.assertRaises(InvalidEventDataError):
            Event("", "2026-08-01", "09:00", "Main Hall")

    def test_invalid_date_format_raises_error(self):
        with self.assertRaises(InvalidEventDataError):
            Event("Hackathon", "01-08-2026", "09:00", "Main Hall")

    def test_invalid_time_format_raises_error(self):
        with self.assertRaises(InvalidEventDataError):
            Event("Hackathon", "2026-08-01", "9:00am", "Main Hall")

    def test_empty_location_raises_error(self):
        with self.assertRaises(InvalidEventDataError):
            Event("Hackathon", "2026-08-01", "09:00", "")

    def test_update_event_fields(self):
        event = Event("Hackathon", "2026-08-01", "09:00", "Main Hall")
        event.update(title="Hackathon 2.0", location="Auditorium")
        self.assertEqual(event.title, "Hackathon 2.0")
        self.assertEqual(event.location, "Auditorium")

    def test_to_tuple(self):
        event = Event("Hackathon", "2026-08-01", "09:00", "Main Hall", "desc")
        self.assertEqual(
            event.to_tuple(),
            ("Hackathon", "2026-08-01", "09:00", "Main Hall", "desc"),
        )


if __name__ == "__main__":
    unittest.main()
