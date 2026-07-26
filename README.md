# Campus Event Reminder

A console-based Campus Event Reminder application built in Python using
Object-Oriented Programming (OOP) and SQLite for persistent storage.

## Features

- Add, view, edit, and delete campus events
- Input validation for event title, date, time, and location
- Persistent storage using SQLite (`campus_events.db`)
- Upcoming event reminders (next 7 days by default)
- Unit tests for both the Event and Database modules

## Project Structure

```
campus-event-reminder/
│
├── main.py                 # Application entry point (Member 1)
├── event.py                 # Event class + validation (Member 2)
├── database.py               # SQLite database logic (Member 3)
├── menu.py                   # Console user interface (Member 4)
├── notification.py           # Reminder/notification logic (Member 5)
├── tests/
│   ├── test_event.py
│   └── test_database.py
├── events.db                 # Created automatically on first run
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.8 or later
- No external packages required (uses only the standard library:
  `sqlite3`, `datetime`, `unittest`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sagelessly/Group11-campus-event-reminder.git
   cd Group11-campus-event-reminder
   ```

2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   No external packages or installation required! The application runs entirely on Python's standard built-in libraries (`sqlite3`, `datetime`, `unittest`).

## Running the Application

```
python main.py
```

You will see a menu like this:

```
===== CAMPUS EVENT REMINDER =====
1. Add Event
2. View All Events
3. Edit Event
4. Delete Event
5. View Upcoming Reminders
6. Exit
==================================
```

Follow the prompts to manage your campus events. The database file
`campus_events.db` is created automatically in the project folder the first
time the app runs.

## Running Tests

From the project root:

```
python -m unittest discover -s tests
```

## Standalone Reminders

You can run the notification module on its own (for example, via a
scheduled task or cron job) to print upcoming reminders without
opening the full menu:

```
python notification.py
```

## Team Contributions

| Member | Responsibility                                   |
|--------|---------------------------------------------------|
| 1      | Project setup, `main.py`, integration             |
| 2      | `event.py`, event validation, unit tests           |
| 3      | `database.py`, SQLite schema and CRUD operations   |
| 4      | `menu.py`, console UI, feature testing             |
| 5      | `notification.py`, documentation, deployment guide |

## Screenshots

See the `screenshots/` folder for sample runs of the application.
