import telebot
import json
from binance.client import Client
import time
from termcolor import colored
import requests
import os

try:
    with open("credentials.json", "r") as f:
        credentials2 = json.load(f)
except:
    print("Перевірте наявність файла credentials.json")


client = Client(credentials2["api_key"], credentials2["secret_key"])

def buy_order():
    #ця функція буде купувати
    print("nothing")

def buy_futures(ticker, msg_id):
    try:
        with open("taapi_credentials.json", "r") as f:
            credentials = json.load(f)
    except:
        print("Перевірте наявність файла taapi_credentials.json")
    #тест тільки з RSI
    endpoint = 'https://api.taapi.io/rsi'
    parameters = {
        'secret': credentials["api_key"],
        'exchange': 'binance',
        'symbol': ticker,
        'interval': '1m'
     }
    while (True):
        response = requests.get(url = endpoint, params = parameters)
        result = response.json()
        print(result['value'])
        if int(result['value']-20)<50:
            time.sleep(8)
            first_value = result['value']
            #починаємо моніторити відскок РСІ в іншому напрямку
            while (True):
                response2 = requests.get(url = endpoint, params = parameters)
                result2 = response2.json()
                second_value = result2['value']
                print("in other loop",result2['value'])
                if second_value>first_value:
                    buy_order()
                    info = client.get_symbol_ticker(symbol = ticker.replace('/', ''))
                    print (info['price'])
                    stroka = "Я буду купувати: RSI= " +str(result2['value'])+"  Price= "+str(info['price'])
                    bot.send_message(msg_id, stroka)
                    break
                first_value = second_value
                time.sleep(8)
        time.sleep(8)

bot = telebot.TeleBot('1529609010:AAFcB0xEhlMtpL7NYbVs0AWDXiXxI-zC7EM')

#bot.send_message('@yfedeiko', "Hello!")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('EOS/USDT', 'XLM/USDT', 'XRP/USDT', 'DASH/USDT', 'ADA/USDT')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Зупинка')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, цей бот вміє торгувати на Binance, Просто відправ тікер', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if (message.text=="Зупинка"):
        bot.send_message(message.chat.id, 'Кінець...')
        os._exit(os.EX_OK)
    else:
        try:
            bot.send_message(message.chat.id, 'Пооооїхалиии...', reply_markup=keyboard2)
            buy_futures(message.text.upper(), message.chat.id)
        except:
            bot.send_message(message.chat.id, 'Сталася внутрішня проблема, перезапустіть бота')

bot.polling()
