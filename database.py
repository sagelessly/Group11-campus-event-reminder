"""
database.py
Member 3 - Database & Data Storage Module

Handles all SQLite database operations for Campus Event Reminder:
table creation, and saving, retrieving, updating, and deleting events.
"""

import sqlite3
from contextlib import contextmanager

from event import Event

DB_NAME = "events.db"


@contextmanager
def get_connection(db_name=DB_NAME):
    """Context manager that opens a connection, commits, and always closes it."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_name=DB_NAME):
    """Create the events table if it doesn't already exist."""
    with get_connection(db_name) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT
            )
            """
        )


def add_event(event: Event, db_name=DB_NAME):
    """Insert a new event into the database and return its generated id."""
    with get_connection(db_name) as conn:
        cursor = conn.execute(
            """
            INSERT INTO events (title, date, time, location, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            event.to_tuple(),
        )
        event.event_id = cursor.lastrowid
        return event.event_id


def get_all_events(db_name=DB_NAME):
    """Return a list of Event objects, sorted by date then time."""
    with get_connection(db_name) as conn:
        rows = conn.execute("SELECT * FROM events ORDER BY date, time").fetchall()
    return [_row_to_event(row) for row in rows]


def get_event_by_id(event_id, db_name=DB_NAME):
    """Return a single Event by id, or None if it doesn't exist."""
    with get_connection(db_name) as conn:
        row = conn.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()
    return _row_to_event(row) if row else None


def update_event(event_id, db_name=DB_NAME, **fields):
    """Update one or more fields of an event by id. Returns True on success."""
    existing = get_event_by_id(event_id, db_name)
    if not existing:
        return False

    existing.update(**fields)

    with get_connection(db_name) as conn:
        conn.execute(
            """
            UPDATE events
            SET title = ?, date = ?, time = ?, location = ?, description = ?
            WHERE event_id = ?
            """,
            (*existing.to_tuple(), event_id),
        )
    return True


def delete_event(event_id, db_name=DB_NAME):
    """Delete an event by id. Returns True if a row was deleted."""
    with get_connection(db_name) as conn:
        cursor = conn.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
        return cursor.rowcount > 0


def _row_to_event(row):
    """Convert a sqlite3.Row into an Event object."""
    return Event(
        title=row["title"],
        date=row["date"],
        time=row["time"],
        location=row["location"],
        description=row["description"],
        event_id=row["event_id"],
    )