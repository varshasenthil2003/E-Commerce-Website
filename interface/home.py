from twilio.rest import Client

account_sid = "AC1f31f4290992152707ab1a0515d45d10"
auth_token = "b7448da728232da2f69c2fed686ae4e6"

# Create a Twilio client instance
client = Client(account_sid, auth_token)

# The phone number you want to send the SMS to (must be verified with Twilio)

to_phone_number = "+919486164890"

# The phone number you want to send the SMS from (must be a Twilio number)
from_phone_number = "+917339391122"

# The message you want to send
message = "Hello, World!"

# Send the SMS message
message = client.messages.create(
    to=to_phone_number,
    from_=from_phone_number,
    body=message)

print("SMS sent successfully!")