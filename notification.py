"""
notification.py
Member 5 - Notifications, Documentation & Deployment Module

Provides reminder functionality for upcoming campus events.
Can be run standalone (e.g. scheduled via cron or Task Scheduler)
to print reminders for events happening soon.
"""

from datetime import datetime, timedelta

import database


def get_upcoming_events(days_ahead=7, db_name=database.DB_NAME):
    """Return events occurring between now and `days_ahead` days from now."""
    now = datetime.now()
    cutoff = now + timedelta(days=days_ahead)

    all_events = database.get_all_events(db_name)
    upcoming = [
        event for event in all_events
        if now <= event.get_datetime() <= cutoff
    ]
    return upcoming


def print_reminders(days_ahead=7):
    """Print reminders directly to the console."""
    upcoming = get_upcoming_events(days_ahead)
    if not upcoming:
        print("No upcoming events to remind you about.")
        return

    event_word = "event" if len(upcoming) == 1 else "events"
    print(f"You have {len(upcoming)} {event_word} coming up in the next {days_ahead} day(s):")
    for event in upcoming:
        days_left = (event.get_datetime() - datetime.now()).days
        day_word = "day" if days_left == 1 else "days"
        print(f" - {event.title} on {event.date} at {event.time} ({days_left} {day_word} left)")


if __name__ == "__main__":
    print_reminders()
