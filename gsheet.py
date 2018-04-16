import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)

gc = gspread.authorize(credentials)


def write_google_sheet(labels):
    # Open a worksheet from spreadsheet with one shot
    wks = gc.open("Lambda Image Rekognition").sheet1

    for label in labels:
        print(label)
        values = list(label.values())
        values.append(str(datetime.datetime.now()))
        wks.append_row(values)


def write_google_sheet_celebrity(celebrities):
    wks = gc.open("Lambda Image Rekognition").worksheet("Celebrities")

    for celeb in celebrities:
        values = [celeb.get('Name'), celeb.get('MatchConfidence')]

        wks.append_row(values)
