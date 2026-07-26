"""
menu.py
Member 4 - User Interface & Testing Module

Console-based menu that connects the user to the Event and Database modules.
"""

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


def prompt_event_details():
    title = input("Title: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM, 24h): ").strip()
    location = input("Location: ").strip()
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


def edit_event_ui():
    print("\n-- Edit Event --")
    view_events_ui()
    try:
        event_id = int(input("Enter the ID of the event to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    existing = database.get_event_by_id(event_id)
    if not existing:
        print("Event not found.")
        return

    print("Leave a field blank to keep its current value.")
    title = input(f"Title [{existing.title}]: ").strip() or None
    date = input(f"Date [{existing.date}]: ").strip() or None
    time = input(f"Time [{existing.time}]: ").strip() or None
    location = input(f"Location [{existing.location}]: ").strip() or None
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
