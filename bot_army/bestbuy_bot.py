from bot_army.stock_bot_base import StockBot
import requests


class BestBuyBot(StockBot):

    def __init__(self, twilio):
        self.received_error_response = False
        self.twilio = twilio
        self.sku_watch_list = [
            '6430175',
            '6429440',
            '6432399',
            '6414104'  #  in stock
        ]
        super().__init__()

    def send_error_notification(self):
        self.twilio.send_text_to_all('Received error response on BestBuy')

    def send_recovery_notification(self):
        self.twilio.send_text_to_all('Recovered from error response on BestBuy')

    def send_carted_notification(self, sku):
        self.twilio.send_text_to_all('THIS IS NOT A DRILL! GO GO GO! In stock at BestBuy. '
                                     'https://www.bestbuy.com/site/{}.p'.format(sku))

    # TODO: How can I hit their API more frequently? Change some id? IP?
    def check_add_to_cart(self, sku):
        url = "https://www.bestbuy.com/cart/api/v1/addToCart"
        payload = '{{\"items\":[{{\"skuId\":\"{}\"}}]}}'.format(sku)
        headers = {
            'authority': 'www.bestbuy.com',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://www.bestbuy.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.bestbuy.com/site/nvidia-geforce-rtx-2070-super-8gb-gddr6-pci-express-3-0-graphics-card-black-silver/6361328.p?skuId=6361328',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'UID=8386bdc4-dca2-47be-8b10-aa961fe59788; physical_dma=602; oid=515510334; vt=cc9f32bd-faf8-11ea-ab9a-0ed897ac9bb7; globalUserTransition=cba; bm_sz=04968E157A6BE3042C1BF065B1EF6883~YAAQX6g4Fyo3Yp90AQAAKRu/qQnSSp+iLbp1pAHSLT5686lCd+aAHR4ucu0P97H6XGJoNsp6PSuRcgRnNjkmRnret/+r8eBm9m6yfYEF57REnwBVj+zjb39aWbKpkut5jld/HLbF3+3vl0mI3OSO7muX9YNqR5wB6qR4l3RgziCm7I3oEg/e4xoGtez6eUan0w==; bby_rdp=l; CTT=0b992bb99531294cf300e24911facaa6; SID=d04b73b8-22e8-4acd-a4e3-601cd6cb14e9; optimizelyEndUserId=oeu1600575709275r0.7476956151892178; COM_TEST_FIX=2020-09-20T04%3A21%3A49.978Z; 52245=; c6db37d7c8add47f1af93cf219c2c682=299b5d0f5fe04d1bee5a23e0aa670e62; tfs_upg=true; AMCVS_F6301253512D2BDB0A490D45%40AdobeOrg=1; s_ecid=MCMID%7C03079084082330615612297113765658364005; _cs_mk=0.7609496472426633_1600575717812; s_cc=true; aam_uuid=09658761331010615311639995147232485703; _cs_c=1; _gcl_au=1.1.2023926168.1600575719; CTE22=T; CRTOABE=1; bby_loc_lb=p-loc-e; customerZipCode=60607|Y; rxVisitor=16005761242211ELKONJJ6R23N4VQI6FTSFTEE3V68TN4; cst_lb=p-cart-cloud; bby_cbc_lb=p-browse-e; CartItemCount=4; bby_prc_lb=p-prc-e; ZPLANK=d5aed3ae1b714b53b560a6fc7751dba5; bby_idn_lb=p-idn-b; ui=1600576651083; G_ENABLED_IDPS=google; pt=2755728180; locDestZip=98125; DYN_USER_CONFIRM=bdda537ab90fef11b8c45361e3e66628; DYN_USER_ID=ATG25643127852; ut=6082c015-766a-11e4-85bb-00505692405b; at=eyJhY2Nlc3NUb2tlbiI6IllXTXRDVGprTFByN0VlcXFDZ0JRVnE0QVdrLTZZekJMNlAtN3ZjRDdrNi10bFRRTWpWNDFBQUFBQUFBQUFBQSIsInRpbWVUb0xpdmUiOjE4MDAsImlzc3VlZFRpbWVzdGFtcCI6MTYwMDU3NjY2ODY2OCwiYXNzZXJ0aW9uIjoidTpTQ1hLX2dnRVRoaGJlNF9PRVg0UkdTS3d5SmZmTk5wbkswX0JYVlQxaFEwIiwicHJpbmNpcGFsIjoidTpTQ1hLX2dnRVRoaGJlNF9PRVg0UkdTS3d5SmZmTk5wbkswX0JYVlQxaFEwIiwicHJpbmNpcGFsSWRlbnRpZmllciI6IjYwODJjMDE1LTc2NmEtMTFlNC04NWJiLTAwNTA1NjkyNDA1YiIsImNvbnN1bWFibGUiOmZhbHNlLCJ2ZXJzaW9uIjoiMS4wIn0.L2YaElmNvG1HFMHUYiP-RsPgtmQTxY-eOqTjOX8rHXVbtuUv7mPCUUGq0PXBippaYDBl5sAltLeHYHnGqmZogA; ltc=10130; basketTimestamp=1600576671118; dtPC=31$376669373_604h-vWPBIIFOUDTQNPHBLEACCUMQESCQBCOUH-0e2; _abck=4D88F333470520A18432A341787EC46A~0~YAAQJqg4F1ZsXad0AQAAGNDNqQT8oYUHSgZrGxNckxBSaKVzHLIlwH0a2hWkqnFYFscRs9b8ObyVHrUM6Z+m7bplnOxNwglcRYAiJvKoxzwORyblaaZG0HDIWlTEAdgDzVacgY52rFwU5+BH+MRlPBGho8vbAqsu3AvWQBn3nywxVDzdLoiZBbJEBsQGhF/hMM0MWo7uusyVKbJSvl4kvrVEUxg3DpWAC8ahKxsik5ZTzXp7xEIrqTkqURac8xVetKXksOumxNPXanLv91KBID0O9/3JHFU8TcahrTbnhYBxJIm3oY16zhVmJD4o1NWEOzj4NTuBjvU=~-1~||-1||~-1; aamoptsegs=aam%3D9208968; dtLatC=2; dtSa=true%7CC%7C-1%7CBestBuy.com%20Logo%7C-%7C1600576686822%7C376669373_604%7Chttps%3A%2F%2Fwww.bestbuy.com%2Fcart%7CCart%20-%20Best%20Buy%7C1600576672612%7C%7C; dtCookie=v_4_srv_31_sn_TLPEE8D0ONVRO6G2BGCLHRIEIJ08A5S3_app-3Ae82a6d064c2ef554_1_ol_0_perc_100000_mul_1; pst2=477; bby_prf_lb=p-prf-b; locStoreId=477; rxvt=1600578488211|1600576124226; bby_trace_id=0.26a83817.1600576726.2e42531; sc-location-v2=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222020-09-20T04%3A28%3A00.927Z%22%2C%22ModifiedAt%22%3A%222020-09-20T04%3A38%3A45.635Z%22%2C%22ExpiresAt%22%3A%222021-09-20T04%3A38%3A45.635Z%22%7D%2C%22value%22%3A%22%7B%5C%22physical%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2298125%5C%22%2C%5C%22source%5C%22%3A%5C%22C%5C%22%2C%5C%22captureTime%5C%22%3A%5C%222020-09-20T04%3A38%3A45.297Z%5C%22%7D%2C%5C%22store%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2298036%5C%22%2C%5C%22searchZipCode%5C%22%3A%5C%2260601%5C%22%2C%5C%22storeId%5C%22%3A%5C%22477%5C%22%2C%5C%22storeHydratedCaptureTime%5C%22%3A%5C%222020-09-20T04%3A38%3A45.634Z%5C%22%2C%5C%22userToken%5C%22%3A%5C%226082c015-766a-11e4-85bb-00505692405b%5C%22%7D%2C%5C%22destination%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2298125%5C%22%7D%7D%22%7D; c2=Computers%20%26%20Tablets%3A%20Computer%20Cards%20%26%20Components%3A%20GPUs%20%2F%20Video%20Graphics%20Cards%3A%20pdp; AMCV_F6301253512D2BDB0A490D45%40AdobeOrg=1585540135%7CMCMID%7C03079084082330615612297113765658364005%7CMCAAMLH-1601181529%7C7%7CMCAAMB-1600576728%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1600582918s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1782005562%7CvVersion%7C4.4.0; _cs_id=5c7e1a51-efc8-a995-8e86-345a916822d2.1600575718.1.1600576729.1600575718.1.1634739718461.Lax.0; _cs_s=12.1; s_sq=bbymainprod%3D%2526pid%253DComputers%252520%252526%252520Tablets%25253A%252520Computer%252520Cards%252520%252526%252520Components%25253A%252520GPUs%252520%25252F%252520Video%252520Graphics%252520Cards%25253A%252520pdp%2526pidt%253D1%2526oid%253Dfunctiontc%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DBUTTON; vt=cc9f32bd-faf8-11ea-ab9a-0ed897ac9bb7; cst_lb=p-cart-cloud; _abck=4D88F333470520A18432A341787EC46A~-1~YAAQBAforF5Y4Jh0AQAA9Vc/qgTm5rMVaEmEiIIujLk5mkzEGtJV+CTw7YFgzxzmYNqiGCwJtN36nduD34+/x3401qpersfU8lBVTVSaTVaaqwXwdsqfCg/MpN8y9dPvJ7Yppav7D8rNj0bKcAMPkQXhwHq+vSjNBg8+qQ6DXN9a2ditRXKFGCxCV6fYufGg0m/DG2VGl9Ctc8jM0NyIhfQqq0ePP4s9E/ISrC7xnijFDZvBTiC73hoOR1LCQolZneUsD9DBY5LfdRE1+N0I7oNW50nJzh/8d/dJ1uhHakXiwvfmTQ8WgSoFu+ydyIiMAfWjygHpFfg=~0~-1~-1; CartItemCount=9; basketTimestamp=1600584112072'
        }
        print(f'checking availability for {sku}')
        response = requests.request("POST", url, headers=headers, data=payload)
        self.set_error_message_flag(response)

        response_dict = response.json()
        print(response_dict)
        if 'errorSummary' not in response_dict:
            self.send_carted_notification(sku)

    def set_error_message_flag(self, response):
        status_code = response.status_code
        successful_message = status_code == 200 or (status_code == 400 and response.json()['errorSummary']['errorCode'] == 'ITEM_NOT_SELLABLE')

        if not successful_message and not self.received_error_response:
            self.received_error_response = True
            self.send_error_notification()
        elif successful_message and self.received_error_response:
            self.received_error_response = False
            self.send_recovery_notification()
