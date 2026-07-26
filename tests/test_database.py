"""
tests/test_database.py
Member 3 - Unit tests for the database module.

Uses a temporary test database file so it never touches the real events.db.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
from event import Event

TEST_DB = "test_events.db"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        database.init_db(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_add_and_get_event(self):
        event = Event("Career Fair", "2026-09-10", "10:00", "Gym")
        event_id = database.add_event(event, TEST_DB)
        fetched = database.get_event_by_id(event_id, TEST_DB)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "Career Fair")

    def test_get_all_events(self):
        database.add_event(Event("Event A", "2026-09-01", "09:00", "Room 1"), TEST_DB)
        database.add_event(Event("Event B", "2026-09-02", "10:00", "Room 2"), TEST_DB)
        events = database.get_all_events(TEST_DB)
        self.assertEqual(len(events), 2)

    def test_update_event(self):
        event_id = database.add_event(Event("Old Title", "2026-09-01", "09:00", "Room 1"), TEST_DB)
        success = database.update_event(event_id, TEST_DB, title="New Title")
        self.assertTrue(success)
        updated = database.get_event_by_id(event_id, TEST_DB)
        self.assertEqual(updated.title, "New Title")

    def test_delete_event(self):
        event_id = database.add_event(Event("To Delete", "2026-09-01", "09:00", "Room 1"), TEST_DB)
        success = database.delete_event(event_id, TEST_DB)
        self.assertTrue(success)
        self.assertIsNone(database.get_event_by_id(event_id, TEST_DB))

    def test_update_nonexistent_event_returns_false(self):
        success = database.update_event(9999, TEST_DB, title="Nothing")
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
