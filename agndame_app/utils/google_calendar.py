import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GoogleCalendarManager:
    
    def __init__(self):
        self.service = self._autheticate()

    # Metodo para autenticarse
    def autheticate(self):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
    def create_event(self, summary, start_time, end_time, timezone, attendees=None):

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
            print 'Event created: %s' % (event.get('htmlLink'))
        except HttpError as error:
            print(f"An error has ocurred: {error}")


    # Metodo para actualizar un evento:
    def update_event(self, event_id, summary=None, start_time=None, end_time=None):ç
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
