import requests
from twilio.rest import Client
import time
import argparse

nvidia_url = "https://store.nvidia.com/store/nvidia/en_US/buy/productID.5438481700/clearCart.yes/nextPage.QuickBuyCartPage"

class TwilioTexter:
    def __init__(self, twilio_account, twilio_token, twilio_number, numbers):
        self.twilio_account = twilio_account
        self.twilio_token = twilio_token
        self.twilio_number = twilio_number
        self.client = Client(twilio_account, twilio_token)
        self.numbers = numbers

    def send_text(self, number_to_text, message):
        # the following line needs your Twilio Account SID and Auth Token

        # change the "from_" number to your Twilio number and the "to" number
        # to the phone number you signed up for Twilio with, or upgrade your
        # account to send SMS to any phone number
        self.client.messages.create(to=number_to_text,
                               from_= self.twilio_number,
                               body=message)

    def send_text_to_all(self, message):
        for number_to_text in numbers:
            self.client.messages.create(to=number_to_text,
                                   from_= self.twilio_number,
                                   body=message)

class StockChecker:
    def __init__(self, twilio):
        self.received_error_response = False
        self.twilio = twilio

    def set_error_message_flag(self, status_code):
        if status_code != 200 and not self.received_error_response:
            self.received_error_response = True
            self.twilio.send_text_to_all('Received error response from NVIDIA')
        elif status_code == 200 and self.received_error_response:
            self.received_error_response = False
            self.twilio.send_text_to_all('Recovered from error response')

    def is_out_of_stock(self):
        payload = {}
        headers = {}
        response = requests.request("GET", nvidia_url, headers=headers, data = payload)
        self.set_error_message_flag(response.status_code)
        return response.text.count('sorry but NVIDIA GEFORCE RTX 3080 is currently out of stock')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--twilio_account_number', help='twilio account number')
    parser.add_argument('--twilio_token', help='twilio account token')
    parser.add_argument('--twilio_number', help='twilio number to recieve text from')
    parser.add_argument('--numbers', help='comma separated numbers with extension. ex) +12223334444')
    parser.add_argument('--stock_check_interval', help='seconds to wait between stock checks')

    args = parser.parse_args()
    numbers = args.numbers.split(',')
    stock_check_interval = int(args.stock_check_interval)

    twilio = TwilioTexter(args.twilio_account_number, args.twilio_token, args.twilio_number, numbers)
    stock_checker = StockChecker(twilio)

    twilio.send_text(numbers[0], 'started listening')

    while 1:
        if not stock_checker.is_out_of_stock():
            twilio.send_text_to_all(f'RED ALERT! THIS IS NOT A DRILL! GO GO GO! {nvidia_url}')
        time.sleep(stock_check_interval)