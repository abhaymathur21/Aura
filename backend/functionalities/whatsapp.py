# Install twilio package if you haven't already
# pip install twilio

from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()

# Twilio Account SID and Auth Token
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')


def send_message(message_text):
    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Your WhatsApp number and recipient's WhatsApp number
    whatsapp_from = 'whatsapp:+14155238886'  # Twilio Sandbox number
    whatsapp_to = 'whatsapp:+919920980869'  # Recipient's WhatsApp number

    # Message content
    # message_text = input("Enter the message you want to send:")

    try:
        # Send the message
        message = client.messages.create(body=message_text,
                                        from_=whatsapp_from,
                                        to=whatsapp_to)
        print("Message sent successfully!")
        print("Message SID:", message.sid)
    except Exception as e:
        print("An error occurred:", str(e))
