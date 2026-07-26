"""
event.py
Member 2 - Event Management Module

Defines the Event class and validation logic for Campus Event Reminder.
"""

from datetime import datetime


class InvalidEventDataError(Exception):
    """Custom exception raised when event data fails validation."""
    pass


class Event:
    """Represents a single campus event."""

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"

    def __init__(self, title, date, time, location, description="", event_id=None):
        self.event_id = event_id
        self.title = self._validate_title(title)
        self.date = self._validate_date(date)
        self.time = self._validate_time(time)
        self.location = self._validate_location(location)
        self.description = description.strip() if description else ""

    # ---------- Validation methods ----------
    @staticmethod
    def _validate_title(title):
        if not title or not str(title).strip():
            raise InvalidEventDataError("Event title cannot be empty.")
        return str(title).strip()

    @staticmethod
    def _validate_date(date_str):
        try:
            datetime.strptime(date_str, Event.DATE_FORMAT)
        except (ValueError, TypeError):
            raise InvalidEventDataError(
                f"Invalid date '{date_str}'. Use format YYYY-MM-DD."
            )
        return date_str

    @staticmethod
    def _validate_time(time_str):
        try:
            datetime.strptime(time_str, Event.TIME_FORMAT)
        except (ValueError, TypeError):
            raise InvalidEventDataError(
                f"Invalid time '{time_str}'. Use 24-hour format HH:MM."
            )
        return time_str

    @staticmethod
    def _validate_location(location):
        if not location or not str(location).strip():
            raise InvalidEventDataError("Event location cannot be empty.")
        return str(location).strip()

    # ---------- Utility methods ----------
    def get_datetime(self):
        """Return a combined datetime object, useful for sorting and reminders."""
        return datetime.strptime(
            f"{self.date} {self.time}", f"{self.DATE_FORMAT} {self.TIME_FORMAT}"
        )

    def to_tuple(self):
        """Return event data as a tuple, useful for DB insertion/updates."""
        return (self.title, self.date, self.time, self.location, self.description)

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "description": self.description,
        }

    def update(self, title=None, date=None, time=None, location=None, description=None):
        """Update fields with validation, only changing the fields provided."""
        if title is not None:
            self.title = self._validate_title(title)
        if date is not None:
            self.date = self._validate_date(date)
        if time is not None:
            self.time = self._validate_time(time)
        if location is not None:
            self.location = self._validate_location(location)
        if description is not None:
            self.description = description.strip()

    def __str__(self):
        return (
            f"[{self.event_id}] {self.title} | {self.date} {self.time} "
            f"@ {self.location}\n    {self.description}"
        )

    def __repr__(self):
        return f"Event({self.title!r}, {self.date!r}, {self.time!r}, {self.location!r})"
