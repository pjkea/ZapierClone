import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time


def send_email_chat():
    """ChatGpt suggestion for send email function"""
    # Email Credentials
    sender_address = 'nsafulansahk@gmail.com'
    sender_password = 'jhfs tudo ubby kjzv'
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

    # Create SMTP session for sending the mail
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
        session.ehlo()
        session.starttls() # enable security
        session.login(sender_address, sender_password) # login with mail_id and password
        text = msg.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(f'Failed to send email: {e}')


send_email_chat()


    