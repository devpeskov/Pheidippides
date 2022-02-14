import telebot
import config
import requests
from decimal import Decimal
import asyncio
import aioschedule as schedule
import time
import random

bot = telebot.TeleBot(config.TOKEN)


def sendCurrency(chat='-1001215138602'):
    msg = 'Ныне курс такой:\n\n'
    msg += getCryptoSchedule('bitcoin', 'Биток биток биточек')
    msg += getCryptoSchedule('ethereum', 'Бутырка')
    msg += getCryptoSchedule('monero', 'Нидзямонета')

    stickerName = str(random.randrange(1, 19))
    sti = open(f'static/{stickerName}.webp', 'rb')
    bot.send_sticker(chat, sti)
    bot.send_message(chat, msg)
    # fpc = '-1001215138602'
    # fpooop = '-1001691787586'


def getCryptoSchedule(cryptoName, message, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
            ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    change_24h = round(float(json["price_change_percentage_24h"]), 2)

    str = (
        f'{message}: {local_price} ({change_24h:+})\n'
    )
    return str


def getCrypto(cryptoName, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
            ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    return local_price


schedule.every(10).seconds.do(sendCurrency)
# schedule.every(10).minutes.do(sendCurrency)
# schedule.every().hour.do(sendCurrency)
# schedule.every().day.at("10:30").do(sendCurrency)
# schedule.every(5).to(10).minutes.do(sendCurrency)
# schedule.every().monday.do(sendCurrency)
# schedule.every().wednesday.at("13:15").do(sendCurrency)
# schedule.every().minute.at(":17").do(sendCurrency)

loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(0.1)


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


@bot.message_handler(content_types=['text'])
def sendCrypto(message):
    if message.text == 'Кроля, дай монетку':
        msg = f'Ну держи.\n\nБиток биток биточек: {getCrypto("bitcoin")}\n'
        sti = open('static/btc.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, msg)
    elif message.text == 'Кроля, дай многа монеток':
        msg = f'Ох... Ладно\n\nБиток биток биточек: {getCrypto("bitcoin")}\n' \
                  f'Бутырка: {getCrypto("ethereum")}\n' \
                  f'Нидзямонета: {getCrypto("monero")}\n'
        sti = open('static/4.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, msg)
    elif message.text == 'Кроля, что скажешь?':
        bot.send_message(message.chat.id,
                         "Скажу, что сказать надо с буквой 'Ass'")
        sti = open('static/n.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    elif message.text == 'Кроля, а ты милаха':
        sti = open('static/pretty.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    elif message.text == 'Кроля, плюнь в спейса':
        video = open('static/spit.mp4', 'rb')
        bot.send_animation(message.chat.id, video)


# Run
bot.polling(none_stop=True)
