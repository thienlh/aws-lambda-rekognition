import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
g = gspread.authorize(credentials)


def write_labels(labels):
    worksheet = g.open("Lambda Image Rekognition").sheet1
    for label in labels:
        print(label)
        values = list(label.values())
        values.append(str(datetime.datetime.now()))
        worksheet.append_row(values)


def write_celebrities(celebrities):
    worksheet = g.open("Lambda Image Rekognition").worksheet("Celebrities")
    for celeb in celebrities:
        print(celeb)
        values = [celeb.get('Name'), celeb.get('MatchConfidence')]
        worksheet.append_row(values)
