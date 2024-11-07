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

class GoogleSheetManager:
    def __init__(self):
        self.service = self._autheticate()

    # Metodo para autenticarse
    def _autheticate(self):

        creds = None

        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN_SHEETS")

        if client_id and client_secret and refresh_token:
            
            creds = Credentials(
                None,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token",
                scopes=SCOPES
            )

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return build("sheets", "v4", credentials=creds)
        

    # Leer hoja de calculo
    # range:
    #   'Sheet1': Devuelve todos los valores de la hoja Sheet1
    #   'A1:I5' : Devuelve todos los valores dentro del rango especificado
    #   'Sheet1!A:A' : Hace referencia a todas las celdas de la primera columna de la Hoja1
    def read_sheet_range(self, range):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=range)
            .execute()
        )

        values = result.get("values", [])

        if not values:
            print("No data found.")
            return
        else:
            return values

    # Insertar datos en la hoja de calculo
    def insert_data_sheet(self, range, data):

        data = {
            'values': [data]
        }

        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .append(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption="USER_ENTERED", insertDataOption='INSERT_ROWS', body=data)
            .execute()
        )

        if result:
            print("Insertados con exito.")
            return True
        else:
            return 


