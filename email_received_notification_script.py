import os
import pickle
import base64
import imaplib
import email
from email.header import decode_header
from twilio.rest import Client
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Twilio credentials
account_sid = 'ACef935f4b4592a285cd678807f27708f6'
auth_token = '4bb86ac0a963b9dac96d3d6336dd0728'
twilio_phone_number = '+14156826510'
to_phone_number = '+233249795541'

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials2.json'

# Use a unique token file for this script
TOKEN_FILE = 'token_notification.pickle'


# Function to send SMS
def send_sms(body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=to_phone_number
    )
    print(f"SMS sent: {message.sid}")


# Function to get OAuth2 credentials
def get_credentials():
    """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth 2.0 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


# Function to generate OAuth2 string for IMAP authentication
def generate_oauth2_string(email, access_token):
    auth_string = f'user={email}\1auth=Bearer {access_token}\1\1'
    return base64.b64encode(auth_string.encode('ascii')).decode('ascii')


# Function to check for new emails
def check_email():
    try:
        creds = get_credentials()
        auth_string = generate_oauth2_string('jkessiful@gmail.com', creds.token)

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.authenticate('XOAUTH2', lambda x: auth_string)
        mail.select("inbox")

        result, data = mail.search(None, 'UNSEEN')
        mail_ids = data[0].split()

        if mail_ids:
            for num in mail_ids:
                result, msg_data = mail.fetch(num, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject, encoding = decode_header(msg['Subject'])[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                send_sms(f"New Email: {subject}")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Failed to check email: {e}")


# Run the email check once
check_email()


