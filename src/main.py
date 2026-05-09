from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Full calendar access needed for deleting events
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate():
    creds = None

    # Load saved login token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Authenticate if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def get_weekly_recurring_events(service):
    weekly_events = []
    page_token = None

    while True:
        events_result = service.events().list(
            calendarId="primary",
            pageToken=page_token
        ).execute()

        events = events_result.get("items", [])

        for event in events:

            # Skip recurring child instances/exceptions
            if "recurringEventId" in event:
                continue

            # Must be a recurring event
            if "recurrence" not in event:
                continue

            recurrence_rules = event["recurrence"]

            # Only weekly recurring events
            is_weekly = any(
                "FREQ=WEEKLY" in rule
                for rule in recurrence_rules
            )

            if not is_weekly:
                continue

            weekly_events.append(event)

        page_token = events_result.get("nextPageToken")

        if not page_token:
            break

    return weekly_events


def delete_events(service, events):
    deleted_count = 0

    for event in events:
        summary = event.get("summary", "(No Title)")
        event_id = event["id"]

        print(f"Deleting: {summary}")

        try:
            service.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()

            deleted_count += 1

        except HttpError as e:

            # Ignore already-deleted events
            if e.resp.status == 410:
                print(f"Already deleted: {summary}")
            else:
                print(f"Failed to delete: {summary}")
                print(e)

    return deleted_count


def main():
    creds = authenticate()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    print("\nSearching for weekly recurring events...\n")

    weekly_events = get_weekly_recurring_events(service)

    if not weekly_events:
        print("No weekly recurring events found.")
        return

    print("The following weekly recurring events will be deleted:\n")

    for i, event in enumerate(weekly_events, start=1):
        summary = event.get("summary", "(No Title)")
        print(f"{i}. {summary}")

    confirm = input("\nProceed with deletion? (y/n): ").strip().lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    print("\nDeleting events...\n")

    deleted_count = delete_events(service, weekly_events)

    print(f"\nDone. Deleted {deleted_count} weekly recurring event series.")


if __name__ == "__main__":
    main()