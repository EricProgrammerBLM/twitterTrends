acc_sid = ' '
auth_token = ' '
twilio_number = '+17816536124'
target_number = '+1your number goes here'

# Download the helper library from https://www.twilio.com/docs/python/i
#We used Twilio.com. Literally easy set up, and using free trial that gives $15 free
import os
from twilio.rest import Client

client = Client(acc_sid, auth_token)

def SendText(message):
  message = client.messages.create(
    body=message,
    from_=twilio_number,
    to=target_number
                      )



                    