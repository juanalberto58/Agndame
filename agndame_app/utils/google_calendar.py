import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GoogleCalendarManager:
    
    def __init__(self):
        self.service = self._autheticate()

    # Método para autenticarse
    def _autheticate(self):
        creds = None

        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")

        if client_id and client_secret and refresh_token:
            creds = Credentials(
                None,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token"
            )

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return build("calendar", "v3", credentials=creds)


    # Metodo para mostrar eventos
    def list_upcoming_events(self, max_result=10):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_result,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return
        else:
            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])


    # Metodo para crear un evento en google calendar:
    def create_event(self, summary, start_time, end_time, timezone, attendees):

        event = {
            'summary': summary,
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        }

        if attendees:
            event['attendees']=[{'email':email} for email in attendees]

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        except HttpError as error:
            print(f"An error has ocurred: {error}")


    # Metodo para actualizar un evento:
    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        event = self.service.events().instances(calendarId='primary', eventId=event_id).execute()

        if summary:
            event['summary'] = summary
        if start_time:
            event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        if end_time:
            event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        try:
            update_event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            return update_event
        except HttpError as error:
            print(f"An error has ocurred in update_event: {error}")


    # Metodo para borrar un evento:
    def delete_event(self, event_id):
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id, body=event).execute()
        except HttpError as error:
            print(f"An error has ocurred in delete_event: {error}")
