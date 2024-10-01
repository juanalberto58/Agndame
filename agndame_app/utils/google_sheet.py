import os.path
import gspread
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1rwPcUt0jmZAYPecYwh8WmYufC9EMc2NX9TJF2bbS968"
RANGE_NAME = "A1:I5"

class GoogleSheetManager:
    def __init__(self):
        self.service = self._autheticate()

    # Metodo para autenticarse
    def _autheticate(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token_sheet.json"):
            creds = Credentials.from_authorized_user_file("token_sheet.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                CREDENTIALS_PATH = os.path.join(BASE_DIR, '', 'utils', 'credentials.json')

                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
            with open("token_sheet.json", "w") as token:
                token.write(creds.to_json())

        return build("sheets", "v4", credentials=creds)
        

    def read_sheet(self):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
            .execute()
        )

        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        print("Name, Major:")
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(f"{row[0]}, {row[4]}")


