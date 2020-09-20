from twilio.rest import Client


class TwilioTexter:
    def __init__(self, twilio_account, twilio_token, twilio_number, numbers):
        self.twilio_account = twilio_account
        self.twilio_token = twilio_token
        self.twilio_number = twilio_number
        self.client = Client(twilio_account, twilio_token)
        self.numbers = numbers

    def send_text_to_all(self, message):
        for number_to_text in self.numbers:
            self.client.messages.create(
                to=number_to_text,
                from_=self.twilio_number,
                body=message
            )