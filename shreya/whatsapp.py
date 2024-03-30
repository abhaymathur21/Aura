# Install twilio package if you haven't already
# pip install twilio

from twilio.rest import Client

# Twilio Account SID and Auth Token
account_sid = 'YOUR_SID'
auth_token = 'YOUR_TOKEN'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Your WhatsApp number and recipient's WhatsApp number
whatsapp_from = 'whatsapp:+14155238886'  # Twilio Sandbox number
whatsapp_to = 'whatsapp:+917303066988'  # Recipient's WhatsApp number

# Message content
message_text = input()

try:
    # Send the message
    message = client.messages.create(body=message_text,
                                     from_=whatsapp_from,
                                     to=whatsapp_to)
    print("Message sent successfully!")
    print("Message SID:", message.sid)
except Exception as e:
    print("An error occurred:", str(e))
