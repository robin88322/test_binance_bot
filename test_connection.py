import json
from binance.client import Client
import time
from termcolor import colored
import requests

try:
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
except:
    print("Перевірте наявність файла credentials.json")


client = Client(credentials["api_key"], credentials["secret_key"])
# time_res = client.get_server_time()
# print(time_res)


#тест на корреляцію
def correlation_test(ticker1, ticker2, timerange):
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    except:
        print("Перевірте наявність файла credentials.json")
    client = Client(credentials["api_key"], credentials["secret_key"])

    info = client.get_symbol_ticker()
    A1 = list(filter(lambda x:x["symbol"]==ticker1,info))
    A2 = list(filter(lambda x:x["symbol"]==ticker2,info))
    while(True):
        try:
            info = client.get_symbol_ticker()
            B1 = list(filter(lambda x:x["symbol"]==ticker1,info))
            B2 = list(filter(lambda x:x["symbol"]==ticker2,info))
            if (float(B1[0]['price'])-float(A1[0]['price']))<0:
                color1 = 'red'
            else:
                color1 = 'green'
            if (float(B2[0]['price'])-float(A2[0]['price']))<0:
                color2 = 'red'
            else:
                color2 = 'green'

            print(B1[0]['price'], B2[0]['price'], colored(float(B1[0]['price'])-float(A1[0]['price']), color1), colored(float(B2[0]['price'])-float(A2[0]['price']), color2)  )
            return B1[0]['price'], B2[0]['price'], float(B1[0]['price'])-float(A1[0]['price']), float(B2[0]['price'])-float(A2[0]['price'])
            A1 = B1
            A2 = B2
        except:
            print("Connection error")
        time.sleep(timerange)

#1 Рахувати індикатори вручну

#2 Витягувати з постороннього сайту
def buy_futures(ticker, msg_id):
    try:
        with open("taapi_credentials.json", "r") as f:
            credentials = json.load(f)
    except:
        print("Перевірте наявність файла taapi_credentials.json")

    endpoint = 'https://api.taapi.io/rsi'
    parameters = {
        'secret': credentials["api_key"],
        'exchange': 'binance',
        'symbol': 'EOS/USDT',
        'interval': '1m'
     }
    while (True):
        response = requests.get(url = endpoint, params = parameters)
        result = response.json()
        print(result)
        time.sleep(3)

buy_futures("BTC")
