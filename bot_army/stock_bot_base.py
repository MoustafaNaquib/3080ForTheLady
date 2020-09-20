from bot_army.abstract_stock_bot import AbstractStockBot
import time


class StockBot(AbstractStockBot):
    def __init__(self):
        self.received_error_response = False

    def set_error_message_flag(self, response):
        status_code = response.status_code

        if status_code != 200 and not self.received_error_response:
            self.received_error_response = True
            self.send_error_notification()
        elif status_code == 200 and self.received_error_response:
            self.received_error_response = False
            self.send_recovery_notification()

    # TODO: Refactor so bots can async run
    def check_watch_list_items(self, stock_check_interval):
        for item in self.sku_watch_list:
            self.check_add_to_cart(item)
            time.sleep(stock_check_interval)
