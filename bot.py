import requests
import time
sleep_time = 10

def is_out_of_stock():
    url = "https://store.nvidia.com/store/nvidia/en_US/buy/productID.5438481700/clearCart.yes/nextPage.QuickBuyCartPage"
    payload = {}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.text.count('sorry but NVIDIA GEFORCE RTX 3080 is currently out of stock')


if __name__ == "__main__":
    while 1:
        if not is_out_of_stock():
            print('BAYBEE')
        else:
            print('nah')
        time.sleep(sleep_time)