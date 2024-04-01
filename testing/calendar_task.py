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


def add_event(service, event_name, start_datetime, end_datetime=None, is_all_day=False, location=None, recurrence = "does not repeat"):
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
    event["recurrence"] = recurrence

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

# def edit_event(service, event_name, new_event_name=None, new_start_datetime=None, new_end_datetime=None):
#     """
#     Edits an existing event on the user's Google calendar based on the event name.

#     Args:
#         service: The Google Calendar API service object.
#         event_name (str): The name of the event to be edited.
#         new_event_name (str, optional): The new name of the event. Defaults to None.
#         new_start_datetime (str, optional): The new start date and time of the event in ISO 8601 format. Defaults to None.
#         new_end_datetime (str, optional): The new end date and time of the event in ISO 8601 format. Defaults to None.
#     """

#     try:
#         now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
#         events_result = (
#             service.events()
#             .list(
#                 calendarId="primary",
#                 timeMin=now,
#                 maxResults=10,
#                 singleEvents=True,
#                 orderBy="startTime",
#             )
#             .execute()
#         )
#         events = events_result.get("items", [])

#         # Find the event to edit by its name
#         event_to_edit = None
#         for event in events:
#             if event.get("summary") == event_name:
#                 event_to_edit = event
#                 break

#         if event_to_edit is None:
#             print("Event not found.")
#             return

#         # Print the event details for debugging
#         print("Event to edit:")
#         print(event_to_edit)

#         # Create a copy of the event with updated details
#         updated_event = {
#             'summary': new_event_name if new_event_name is not None else event_to_edit['summary'],
#             'start': {
#                 'dateTime': new_start_datetime if new_start_datetime is not None else event_to_edit['start']['dateTime']
#             },
#             'end': {
#                 'dateTime': new_end_datetime if new_end_datetime is not None else event_to_edit['end']['dateTime']
#             }
#         }

#         # Call the patch API to modify the event
#         patched_event = service.events().patch(
#             calendarId='primary',
#             eventId=event_to_edit['id'],
#             body=updated_event
#         ).execute()

#         print(f"Event updated: {patched_event.get('htmlLink')}")

#     except HttpError as error:
#         print(f"An error occurred: {error}")


# if __name__ == "__main__":
#     service = authenticate()

#     # Example usage:
#     top_ten(service)  # Uncomment to view upcoming events

#     # Get event details from the user
#     event_name = input("Enter the event name to edit: ")
#     new_event_name = input("Enter the new event name (press Enter to keep it unchanged): ")
#     new_start_datetime = input("Enter the new start date and time in YYYY-MM-DDTHH:MM:SSZ format (press Enter to keep it unchanged): ")
#     new_end_datetime = input("Enter the new end date and time (optional, same as start time if not provided): ")

#     # Edit the event using the edit_event function
#     edit_event(service, event_name, new_event_name, new_start_datetime, new_end_datetime)

def delete_event_by_name(service, event_name):
    """
    Deletes an event from the user's Google Calendar based on the event name.

    Args:
        service: The Google Calendar API service object.
        event_name (str): The name of the event to be deleted.
    """

    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
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

        # Find the event to delete by its name
        event_to_delete = None
        for event in events:
            if event.get("summary") == event_name:
                event_to_delete = event
                break

        if event_to_delete is None:
            print("Event not found.")
            return

        # Call the delete API to remove the event
        service.events().delete(calendarId='primary', eventId=event_to_delete['id']).execute()

        print("Event deleted successfully.")

    except HttpError as error:
        print(f"An error occurred: {error}")


def update_event(service, event_name, new_event_name=None, new_start_datetime=None, new_end_datetime=None, new_location = None, new_recurrence = None):
  try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
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

        # Find the event by its name
        for event in events:
            if event.get("summary") == event_name:
                # Extract event details
                event_name = event.get("summary")
                # print("event name: ",event_name)
                if not new_event_name:
                  new_event_name = event.get("summary")
                  print("new event name: ",new_event_name)
                if not new_start_datetime:
                  new_start_datetime = event["start"].get("dateTime")
                if not new_end_datetime:
                  new_end_datetime = event["end"].get("dateTime")
                if not new_location:
                  new_location = event.get("location")
                if not new_recurrence:
                  new_recurrence = event.get("recurrence")
        
        delete_event_by_name(service, event_name)
        add_event(service, new_event_name, new_start_datetime, new_end_datetime, location=new_location)

        return None

  except HttpError as error:
      print(f"An error occurred: {error}")
      return None
  

if __name__ == "__main__":
    service = authenticate()

    # Example usage:
    top_ten(service)  # Uncomment to view upcoming events

    # Get event details from the user
    x = int(input("1 for add, 2 for delete, 3 for edit: "))
    if x == 1:
      event_name = input("Enter the event name: ")
      start_datetime = input("Enter the start date and time in YYYY-MM-DDTHH:MM:SSZ format (press Enter to keep it unchanged): ")
      end_datetime = input("Enter the end date and time (optional, same as start time if not provided): ")
      location = input("Enter location (optional): ")
      recurrence = input("Enter recurrence frequence(optional): ")
      add_event(service, event_name, start_datetime, end_datetime=end_datetime, is_all_day=False, location=location, recurrence = recurrence)
      
    elif x==2:
      event_name = input("Enter the event name to delete: ")
      delete_event_by_name(service, event_name)
      
    elif x ==3:
      event_name = input("Enter the event name to edit: ")
      new_event = input("Enter the new event name: ")
      start_datetime = input("Enter the new start date and time in YYYY-MM-DDTHH:MM:SSZ format (press Enter to keep it unchanged): ")
      end_datetime = input("Enter the new end date and time (optional, same as start time if not provided): ")
      location = input("Enter new location (optional): ")
      recurrence = input("Enter recurrence frequence(optional): ")
      update_event(service, event_name, new_event_name=new_event, new_start_datetime=start_datetime, new_end_datetime=end_datetime, new_location = location, new_recurrence = recurrence)


