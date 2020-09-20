from bot_army.stock_bot_base import StockBot
import requests


class BestBuyBot(StockBot):

    def __init__(self, twilio):
        self.received_error_response = False
        self.twilio = twilio

    def send_error_notification(self):
        self.twilio.send_text_to_all('Received error response on BestBuy')

    def send_recovery_notification(self):
        self.twilio.send_text_to_all('Recovered from error response on BestBuy')

    def check_add_to_cart(self):
        pass

    def send_carted_notification(self):
        pass

