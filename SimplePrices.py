import hmac
import hashlib
import time
import requests

def getFills(apiKey, secretKey, product_id):
    timestamp = str(int(time.time()))
    message = timestamp + "GET" + "/api/v3/brokerage/orders/historical/fills"
    signature = hmac.new(secretKey.encode('utf-8'), message.encode('utf-8'), digestmod = hashlib.sha256).digest()

    headers = {
        'accept': 'application/json',
        'CB-ACCESS-SIGN': signature.hex(),
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': apiKey
    }
    params = {'product_id': product_id}

    r = requests.get(url = "https://api.coinbase.com/api/v3/brokerage/orders/historical/fills", params = params, headers = headers)
    # TODO make it handle cursor to get more than 100 fills
    return r.json()['fills']