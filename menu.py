"""
menu.py
Member 4 - User Interface & Testing Module

Console-based menu that connects the user to the Event and Database modules.
"""

import re

import database
from event import Event, InvalidEventDataError


def display_menu():
    print("\n===== CAMPUS EVENT REMINDER =====")
    print("1. Add Event")
    print("2. View All Events")
    print("3. Edit Event")
    print("4. Delete Event")
    print("5. View Upcoming Reminders")
    print("6. Exit")
    print("==================================")


def _validate_title_input(prompt_text):
    """Prompt for a title and re-prompt until it is a non-empty string."""
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("  Title cannot be empty. Please enter a valid title.")
            continue
        return value


def _validate_date_input(prompt_text):
    """Prompt for a date and re-prompt until it matches YYYY-MM-DD format."""
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("  Date cannot be empty. Please enter a date.")
            continue
        if not date_pattern.match(value):
            print("  Invalid date format. Use YYYY-MM-DD (e.g. 2026-08-15).")
            continue
        # Validate that it's a real calendar date via Event's validation
        try:
            Event._validate_date(value)
        except InvalidEventDataError as e:
            print(f"  {e}")
            continue
        return value


def _validate_time_input(prompt_text):
    """Prompt for a time and re-prompt until it matches HH:MM 24h format."""
    time_pattern = re.compile(r"^\d{2}:\d{2}$")
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("  Time cannot be empty. Please enter a time.")
            continue
        if not time_pattern.match(value):
            print("  Invalid time format. Use HH:MM in 24-hour format (e.g. 14:30).")
            continue
        # Validate that it's a real time via Event's validation
        try:
            Event._validate_time(value)
        except InvalidEventDataError as e:
            print(f"  {e}")
            continue
        return value


def _validate_location_input(prompt_text):
    """Prompt for a location and re-prompt until it is a non-empty string."""
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("  Location cannot be empty. Please enter a valid location.")
            continue
        return value


def prompt_event_details():
    """Prompt the user for all event fields with per-field validation."""
    title = _validate_title_input("Title: ")
    date = _validate_date_input("Date (YYYY-MM-DD): ")
    time = _validate_time_input("Time (HH:MM, 24h): ")
    location = _validate_location_input("Location: ")
    description = input("Description (optional): ").strip()
    return title, date, time, location, description


def add_event_ui():
    print("\n-- Add New Event --")
    try:
        title, date, time, location, description = prompt_event_details()
        event = Event(title, date, time, location, description)
        event_id = database.add_event(event)
        print(f"Event added successfully with ID {event_id}.")
    except InvalidEventDataError as e:
        print(f"Error: {e}")


def view_events_ui():
    print("\n-- All Events --")
    events = database.get_all_events()
    if not events:
        print("No events found.")
        return
    for event in events:
        print(event)
        print("-" * 40)


def _prompt_optional(prompt_text, validator_func):
    """
    Prompt the user for an optional field.
    If the input is empty (user pressed Enter), return None (keep existing value).
    Otherwise, run the input through the given validator and re-prompt until valid.
    """
    while True:
        value = input(prompt_text).strip()
        if not value:
            return None
        try:
            return validator_func(value)
        except (InvalidEventDataError, ValueError) as e:
            print(f"  {e}")
            continue


def _validate_optional_title(value):
    """Validate a non-empty title string."""
    return Event._validate_title(value)


def _validate_optional_date(value):
    """Validate a date string matches YYYY-MM-DD format and is a real date."""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        raise InvalidEventDataError(
            "Invalid date format. Use YYYY-MM-DD (e.g. 2026-08-15)."
        )
    return Event._validate_date(value)


def _validate_optional_time(value):
    """Validate a time string matches HH:MM 24h format and is a real time."""
    if not re.match(r"^\d{2}:\d{2}$", value):
        raise InvalidEventDataError(
            "Invalid time format. Use HH:MM in 24-hour format (e.g. 14:30)."
        )
    return Event._validate_time(value)


def _validate_optional_location(value):
    """Validate a non-empty location string."""
    return Event._validate_location(value)


def edit_event_ui():
    print("\n-- Edit Event --")
    view_events_ui()
    try:
        event_id = int(input("Enter the ID of the event to edit: "))
        if event_id <= 0:
            print("Event ID must be a positive number.")
            return
    except ValueError:
        print("Invalid ID.")
        return

    existing = database.get_event_by_id(event_id)
    if not existing:
        print("Event not found.")
        return

    print("Leave a field blank to keep its current value.")
    title = _prompt_optional(
        f"Title [{existing.title}]: ", _validate_optional_title
    )
    date = _prompt_optional(
        f"Date [{existing.date}]: ", _validate_optional_date
    )
    time = _prompt_optional(
        f"Time [{existing.time}]: ", _validate_optional_time
    )
    location = _prompt_optional(
        f"Location [{existing.location}]: ", _validate_optional_location
    )
    description = input(f"Description [{existing.description}]: ").strip() or None

    try:
        success = database.update_event(
            event_id,
            title=title,
            date=date,
            time=time,
            location=location,
            description=description,
        )
        print("Event updated." if success else "Update failed.")
    except InvalidEventDataError as e:
        print(f"Error: {e}")


def delete_event_ui():
    print("\n-- Delete Event --")
    view_events_ui()
    try:
        event_id = int(input("Enter the ID of the event to delete: "))
        if event_id <= 0:
            print("Event ID must be a positive number.")
            return
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input(f"Are you sure you want to delete event {event_id}? (y/n): ").lower()
    if confirm == "y":
        success = database.delete_event(event_id)
        print("Event deleted." if success else "Event not found.")
    else:
        print("Cancelled.")


def reminders_ui():
    from notification import get_upcoming_events

    print("\n-- Upcoming Reminders (next 7 days) --")
    upcoming = get_upcoming_events(days_ahead=7)
    if not upcoming:
        print("No upcoming events in the next 7 days.")
        return
    for event in upcoming:
        print(f"Reminder: {event}")
        print("-" * 40)


def run():
    """Main menu loop. Initializes the database, then handles user choices."""
    database.init_db()
    actions = {
        "1": add_event_ui,
        "2": view_events_ui,
        "3": edit_event_ui,
        "4": delete_event_ui,
        "5": reminders_ui,
    }

    while True:
        display_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    run()