import requests
from twilio.rest import Client
import time
import argparse

sleep_time = 10
nvidia_url = "https://store.nvidia.com/store/nvidia/en_US/buy/productID.5438481700/clearCart.yes/nextPage.QuickBuyCartPage"

class TwilioTexter():

    def __init__(self, twilio_account, twilio_token, twilio_number):
        self.twilio_account = twilio_account
        self.twilio_token = twilio_token
        self.twilio_number = twilio_number
        self.client = Client(twilio_account, twilio_token)

    def send_text(self, number_to_text):
        # the following line needs your Twilio Account SID and Auth Token

        # change the "from_" number to your Twilio number and the "to" number
        # to the phone number you signed up for Twilio with, or upgrade your
        # account to send SMS to any phone number
        self.client.messages.create(to=number_to_text,
                               from_= self.twilio_number,
                               body=f'RED ALERT! THIS IS NOT A DRILL! GO GO GO! {nvidia_url}')


def is_out_of_stock():
    payload = {}
    headers = {}
    response = requests.request("GET", nvidia_url, headers=headers, data = payload)
    return response.text.count('sorry but NVIDIA GEFORCE RTX 3080 is currently out of stock')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument('--twilio_account_number', help='twilio account number')
    parser.add_argument('--twilio_token', help='twilio account token')
    parser.add_argument('--twilio_number', help='twilio number to recieve text from')
    parser.add_argument('--numbers', help='comma separated numbers with extension. ex) +12223334444')

    args = parser.parse_args()

    twilio = TwilioTexter(args.twilio_account_number, args.twilio_token, args.twilio_number)
    numbers = args.numbers.split(',')

    while 1:
        if not is_out_of_stock():
            for number in numbers:
                twilio.send_text(number)
        time.sleep(sleep_time)