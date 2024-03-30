import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]  # Required for event creation

"""
Shows basic usage of the Google Calendar API.

- Prints the start and name of the next 10 events on the user's calendar (top_ten function).
- Adds a new event to the Google calendar with specified details (add_event function).
"""


def authenticate():
    """Authenticates the user and returns the Calendar API service object."""

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def top_ten(service):
    """
    Prints the start and name of the next 10 events on the user's calendar.
    """

    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def add_event(service, event_name, start_datetime, end_datetime=None, is_all_day=False, location=None):
    """
    Adds a new event to the user's Google calendar.

    Args:
        service: The Google Calendar API service object.
        event_name (str): The name of the event.
        start_datetime (str): The start date and time of the event in ISO 8601 format (e.g., 2024-03-31T10:00:00Z).
        end_datetime (str, optional): The end date and time of the event in ISO 8601 format. Defaults to None (same as start_datetime).
        is_all_day (bool, optional): Whether the event is an all-day event. Defaults to False.
        location (str, optional): The location of the event. Defaults to None.
    """

    event = {"summary": event_name}

    if is_all_day:
        event["start"] = {"date": start_datetime.split("T")[0]}  # Extract date for all-day events
        event["end"] = {"date": (datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")}  # Set end date to the next day
    else:
        event["start"] = {"dateTime": start_datetime}
        if end_datetime:
            event["end"] = {"dateTime": end_datetime}

    # Add location if provided
    if location:
        event["location"] = location

    # Set "recurrence" to 'does not repeat' (this is the default behavior, but added for clarity)
    event["recurrence"] = ["does not repeat"]

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")



if __name__ == "__main__":
    service = authenticate()

    # Example usage:
    top_ten(service)  # Uncomment to view upcoming events

    # Get event details from the user
    event_name = input("Enter the event name: ")

    # Get start date and time (assuming ISO 8601 format for consistency)
    start_datetime = input("Enter the start date and time in YYYY-MM-DDTHH:MM:SSZ format (e.g., 2024-03-31T10:00:00Z): ")

    # Optional: Get end date and time (if different from start)
    end_datetime = input(
        "Enter the end date and time (optional, same as start time if not provided): "
    )

    # Create the event using the add_event function
    add_event(service, event_name, start_datetime, end_datetime)

