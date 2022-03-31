import telebot
import config
import requests
from decimal import Decimal
# import asyncio
# import aioschedule as schedule
import schedule
import time
import random
# import multiprocessing
import threading

bot = telebot.TeleBot(config.TOKEN)


# chats-id:
# fpc(default) = '-1001798667684'
# fpooop = '-1001691787586'
# maintainer = '349777242'
def sendCurrency(chat='-1001798667684'):
    dumpJson = requests.get(
        'https://api.coingecko.com/api/v3/coins',
        ).json()
    stickerSwitch = dumpJson[0]['market_data']['price_change_percentage_24h']
    msg = 'Ныне курс такой:\n\n'
    msg += formMessage('bitcoin', 'Батькоин', dumpJson)
    msg += formMessage('ethereum', 'Эфирка', dumpJson)
    msg += formMessage('monero', 'Нидзямонета', dumpJson)

    bot.send_sticker(chat, chooseSticker(stickerSwitch))
    bot.send_message(chat, msg)


def formMessage(cryptoName, message, dumpJson, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    coinJson = []
    for json in dumpJson:
        if json['id'] == cryptoName:
            coinJson = json['market_data']

    local_price = round(Decimal(coinJson["current_price"][f'{baseCurrency}']), 2)
    change_24h = round(float(coinJson["price_change_percentage_24h"]), 2)
    return f'{message}: {local_price} ({change_24h:+})\n'


def chooseSticker(change_24h):
    if change_24h >= 0:
        stickerName = str(random.randrange(1, 7))
        sti = open(f'static/good/{stickerName}.webp', 'rb')
        return sti
    else:
        stickerName = str(random.randrange(1, 13))
        sti = open(f'static/bad/{stickerName}.webp', 'rb')
        return sti


def getCrypto(cryptoName, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
            ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    return local_price


def sendTest(chat='349777242'):
    bot.send_message(chat, 'Testing schedule')


# schedule.every(10).seconds.do(sendCurrency)
# schedule.every(10).minutes.do(sendCurrency)
# schedule.every().hour.do(sendCurrency)
schedule.every(10).seconds.do(sendTest)
schedule.every().day.at("09:30").do(sendTest)
# schedule.every(5).to(10).minutes.do(sendCurrency)
# schedule.every().monday.do(sendCurrency)
# schedule.every().wednesday.at("13:15").do(sendCurrency)
# schedule.every().minute.at(":17").do(sendCurrency)


def sched():
    while True:
        schedule.run_pending()
        time.sleep(1)


sch = threading.Thread(target=sched)
sch.start()


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/robot.webp', 'rb')
    msg = '... Опять работать?! Ну да, я же просто машина, мое дело быть рабом'

    bot.send_message(message.chat.id, msg)
    bot.send_sticker(message.chat.id, sti)
    print(message.chat.id)


@bot.message_handler(commands=['getcrypto'])
def getRequest(message):
    sendCurrency(message.chat.id)


# Run
bot.polling(none_stop=True)
