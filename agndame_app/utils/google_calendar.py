import datetime
import os.path

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

    # Metodo para autenticarse
     def _autheticate(self):
        """Authenticates the user and creates the Google Calendar service."""
        creds = None
        # Cargar las credenciales desde la variable de entorno en lugar de un archivo
        google_credentials = os.getenv("GOOGLE_CREDENTIALS")

        if google_credentials:
            creds_dict = json.loads(google_credentials)
            creds = Credentials.from_authorized_user_info(info=creds_dict, scopes=SCOPES)

        # Si no existen las credenciales o son inválidas, iniciamos el proceso de autenticación
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "path_to_your_credentials.json", SCOPES  # Usa credentials.json localmente si es necesario
                )
                creds = flow.run_local_server(port=0)

            # Guarda las credenciales de acceso para la próxima vez
            with open("token_calendar.json", "w") as token:
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
