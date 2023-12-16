from twilio.rest import Client
import random

account_sid = 'AC1f31f4290992152707ab1a0515d45d10'
auth_token = 'b7448da728232da2f69c2fed686ae4e6'

verify_sid = "VA25045aeae5d3593f6fc88e4796b50431"
verified_number = "+917339391122"

client = Client(account_sid, auth_token)

verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to="+919840615126", channel="sms")
print(verification.status)

otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to="+919840615126", code=otp_code)
print(verification_check.status)