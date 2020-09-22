from bot_army.stock_bot_base import StockBot
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import localtime, strftime, sleep
import random
from user_agent import get_user_agent_list

class BestBuyBot(StockBot):

    def __init__(self, twilio):
        self.received_error_response = False
        self.twilio = twilio
        self.sku_watch_list = [
            '6429440'
        ]
        self.session = requests.Session()
        self.user_agent_list = get_user_agent_list()
        self.requests_since_refresh = 0
        self.cookies = None
        self.total_count = 0
        super().__init__()


    def send_error_notification(self):
        self.twilio.send_text_to_all('Received error response on BestBuy')

    def send_recovery_notification(self):
        self.twilio.send_text_to_all('Recovered from error response on BestBuy')

    def send_carted_notification(self, sku):
        self.twilio.send_text_to_all('THIS IS NOT A DRILL! GO GO GO! In stock at BestBuy. '
                                     'https://www.bestbuy.com/site/{}.p'.format(sku))

    def refresh_cookies_and_session(self):
        # Initiate the browser
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.delete_all_cookies()
        browser.get('https://www.bestbuy.com')
        cookies = browser.get_cookies()
        browser.quit()
        self.session = requests.Session()
        self.cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        self.requests_since_refresh = 0

    def check_add_to_cart(self, sku):
        # Refresh cookies every 6 requests
        if self.requests_since_refresh % 6 == 0:
            self.refresh_cookies_and_session()

        url = "https://www.bestbuy.com/cart/api/v1/addToCart"
        payload = '{{\"items\":[{{\"skuId\":\"{}\"}}]}}'.format(sku)
        headers = {
            'authority': 'www.bestbuy.com',
            'accept': 'application/json',
            'user-agent': random.choice(self.user_agent_list),
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.bestbuy.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.bestbuy.com/site/insignia-6qt-multi-function-pressure-cooker-stainless-steel/626f3602.p?skuId=6263602',
            'accept-language': 'en-US,en;q=0.9',
            'Connection': 'close'
        }

        print('checking sku', sku, 'at', strftime("%Y-%m-%d %H:%M:%S", localtime()))
        response = self.session.post(url, headers=headers, data=payload, cookies=self.cookies)

        # self.set_error_message_flag(response)

        response_dict = response.json()
        print(response_dict)
        self.requests_since_refresh += 1
        self.total_count += 1
        print(self.total_count, 'successful responses')
        if 'errorSummary' not in response_dict:
            self.send_carted_notification(sku)

        wait_time = random.randint(10, 60)
        print('long waiting', wait_time, 'seconds')
        sleep(wait_time)

    def set_error_message_flag(self, response):
        status_code = response.status_code
        successful_message = status_code == 200 or (status_code == 400 and response.json()['errorSummary']['errorCode'] == 'ITEM_NOT_SELLABLE')

        if not successful_message and not self.received_error_response:
            self.received_error_response = True
            self.send_error_notification()
        elif successful_message and self.received_error_response:
            self.received_error_response = False
            self.send_recovery_notification()
