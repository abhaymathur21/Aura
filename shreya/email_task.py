import os.path
from flask import Flask, render_template, request, jsonify,redirect, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient_email, subject, message):
    """Sends an email using the smtplib library.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        message (str): The body of the email.

    Raises:
        Exception: If there is an error sending the email.
    """
    email_host = 'smtp.gmail.com'
    email_port = 587  # TLS port for Gmail
    sender_email = os.environ["sender_email"]  # Replace with your Gmail address
    password = os.environ["password"]  # Replace with your Gmail password (not recommended for production)

    # Create a secure connection with STARTTLS
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, password)
    except Exception as e:
        print(f"Error connecting to SMTP server: {e}")
        raise

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Set the message body as plain text
    msg.attach(MIMEText(message, "plain"))

    # Send the email
    try:
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        smtp_server.quit()



def auth():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    service = build("gmail", "v1", credentials=creds)
    return service
        

def display_mails(service):
    try:
        # Get the Inbox ID
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        inbox_id = None
        for label in labels:
            if label["name"] == "INBOX":
                inbox_id = label["id"]
                break

        # Retrieve the latest emails in the inbox
        results = service.users().messages().list(userId="me", labelIds=[inbox_id], maxResults=10).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No emails found in inbox.")
        else:
            print("Latest emails in inbox:")
            for message in messages:
                msg = service.users().messages().get(userId="me", id=message["id"]).execute()
                # Find the subject line
                for header in msg['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                # Find the sender name (from the 'From' header)
                for header in msg['payload']['headers']:
                    if header['name'] == 'From':
                        sender_name = header['value']
                        break
                print(f"From: {sender_name}")
                print(f"Subject: {subject}")
                print(f"Snippet: {msg['snippet']}\n")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    service = auth()
    
    display_mails(service)  
    # Example usage (replace with your actual credentials and recipient)
    recipient_email = "shreyashah100803@gmail.com"
    subject = "Important Update"
    message = "This is the message content."
    send_email(recipient_email, subject, message)  
