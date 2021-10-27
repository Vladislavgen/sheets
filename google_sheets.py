import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1cvZswLiDo3LfhnA7RcS8vFqacx73RGor-OZ_FtvyLE8'
SAMPLE_RANGE_NAME = 'A1:AA1000'


def main():
    ##### ЭТО ДЛЯ АВТОРИЗАЦИИ В ГУГЛЕ  (НАЧАЛО) #####

    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'my_json_file.json', SCOPES)  # here enter the name of your downloaded JSON file # ВНИМАНИЕ СЮДА!)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    ##### ЭТО ДЛЯ АВТОРИЗАЦИИ В ГУГЛЕ  (КОНЕЦ) #####

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()

    # Тут полученные данные из таблицы
    values_input = result_input.get('values', [])
    print(values_input)

    if not values_input:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values_input:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


main()
df=pd.DataFrame(values_input[1:], columns=values_input[0])
print(df)