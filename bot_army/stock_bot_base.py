from bot_army.abstract_stock_bot import AbstractStockBot


class StockBot(AbstractStockBot):
    def __init__(self):
        self.received_error_response = False

    def set_error_message_flag(self, status_code):
        if status_code != 200 and not self.received_error_response:
            self.received_error_response = True
            self.send_error_notification()
        elif status_code == 200 and self.received_error_response:
            self.received_error_response = False
            self.send_recovery_notification()
