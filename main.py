"""
main.py
Member 1 - Project Lead & Main Application

Entry point that ties together the Event, Database, Menu, and Notification
modules into a single runnable application.
"""

import database
import menu


def main():
    print("Starting Campus Event Reminder application...")
    database.init_db()
    menu.run()


if __name__ == "__main__":
    main()
