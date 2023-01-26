from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
from datetime import date
from datetime import timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """
    gets date data
    """
    today = date.today()
    today_string = date.today().strftime("%Y/%m/%d")
    one_week_ago = (today - (timedelta(weeks = 1))).strftime("%Y/%m/%d") #using timedelta because calculating 7 days ago might go into the previous month
    one_month_ago = datetime.date(today.year, today.month-1, today.day).strftime("%Y/%m/%d")
    six_months_ago = datetime.date(today.year, today.month-6, today.day).strftime("%Y/%m/%d")
    year_ago = datetime.date(today.year-1, today.month, today.day).strftime("%Y/%m/%d")

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        week_results = service.users().messages().list(userId='me', q=f'"in:sent after:{one_week_ago} before:{today_string}"').execute()
        month_results = service.users().messages().list(userId='me', q=f'"in:sent after:{one_month_ago} before:{today_string}"').execute()
        six_month_results = service.users().messages().list(userId='me', q=f'"in:sent after:{six_months_ago} before:{today_string}"').execute()
        year_results = service.users().messages().list(userId='me', q=f'"in:sent after:{year_ago} before:{today_string}"').execute()

        week_messages = week_results.get('messages', [])
        month_messages = month_results.get('messages', [])
        six_months_messages = six_month_results.get('messages', [])
        year_messages = year_results.get('messages', [])

        if not (week_messages or month_messages or six_months_messages or year_messages):
            print('No messages found.')
            return
        else:
            try:
                print('NEW ERA')
                print('------------------------------------------------------------')
                print('One Week:')
                for message in week_messages:
                    print()
                    print(message['id'])
                # print(len(week_messages))
                # print('One Month:')
                # print(len(month_messages))
                # print('Six Months:')
                # print(len(six_months_messages))
                # print('One Year:')
                # print(len(year_messages))
            except:
                print("Uh oh! Data not found")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()