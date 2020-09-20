import argparse
from twilio_texter import TwilioTexter
from bot_army.bestbuy_bot import BestBuyBot

    # def is_out_of_stock(self):
    #     payload = {}
    #     headers = {}
    #     response = requests.request("GET", nvidia_url, headers=headers, data = payload)
    #     self.set_error_message_flag(response.status_code)
    #     return response.text.count('sorry but NVIDIA GEFORCE RTX 3080 is currently out of stock')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('--twilio_account', help='twilio account number')
    parser.add_argument('--twilio_token', help='twilio account token')
    parser.add_argument('--twilio_number', help='twilio number to recieve text from')
    parser.add_argument('--numbers', help='comma separated numbers with extension. ex) +12223334444')
    parser.add_argument('--stock_check_interval', help='seconds to wait between stock checks')

    args = parser.parse_args()
    numbers = args.numbers.split(',')
    stock_check_interval = int(args.stock_check_interval)

    twilio = TwilioTexter(args.twilio_account, args.twilio_token, args.twilio_number, numbers)

    bot_army = [
        BestBuyBot(twilio)
    ]

    # twilio.send_text_to_all('started listening')

    while 1:
        print('at top')
        for bot in bot_army:
            bot.check_watch_list_items(stock_check_interval)