from abc import ABC

class AbstractStockBot(ABC):

    def set_error_message_flag(self, status_code):
        pass

    def send_error_notification(self):
        pass

    def send_recovery_notification(self):
        pass

    def check_add_to_cart(self):
        pass

    def send_carted_notification(self):
        pass

    def check_watch_list_items(self):
        pass

