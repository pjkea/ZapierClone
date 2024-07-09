import os
import pickle
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# import schedule
# import time


# If modifying these scopes, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid
    then the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def send_email_chat():
    """ChatGpt suggestion for send email function"""
    # Email Credentials
    sender_address = 'nsafulansahk@gmail.com'
    # sender_password = 'jhfs tudo ubby kjzv'
    receiver_address = 'jkessiful@gmail.com'

    # Email Content
    subject = 'Daily Report'
    body = 'This is your daily report.'

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Get OAuth2 credentials
    creds = get_credentials()

    #Connect to the Gmail API
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {'raw': raw}

    try:
        service = build('gmail', 'v1', credentials=creds)
        service.users().messages().send(userId='me', body=message).execute()
        print('Mail Sent')
    except Exception as e:
        print(f'Failed to send email: {e}')

    # Create SMTP session for sending the mail
    # try:
    #     session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
    #     session.ehlo()
    #     session.starttls() # enable security
    #     session.login(sender_address, sender_password) # login with mail_id and password
    #     text = msg.as_string()
    #     session.sendmail(sender_address, receiver_address, text)
    #     session.quit()
    #     print('Mail Sent')
    # except Exception as e:
    #     print(f'Failed to send email: {e}')


send_email_chat()


    