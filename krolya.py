import random
# import threading
# import time
from decimal import Decimal

import requests
# import asyncio
# import aioschedule as schedule
# import schedule
import telebot
import json

import config

bot = telebot.TeleBot(config.TOKEN)


with open('static.json') as f:
    media = json.load(f)
    stickers = media.get('stickers')


# chats-id:
# fpc(default) = '-1001798667684'
# maintainer = '349777242'
def sendCurrency(chat='349777242'):
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
    for member_json in dumpJson:
        if member_json['id'] == cryptoName:
            coinJson = member_json['market_data']

    local_price = round(
        Decimal(coinJson["current_price"][f'{baseCurrency}']), 2)
    change_24h = round(float(coinJson["price_change_percentage_24h"]), 2)
    return f'{message}: {local_price} ({change_24h:+})\n'


def chooseSticker(change_24h):
    if change_24h >= 0:
        return str(stickers.get('good').get(f'{random.randrange(1, 7)}'))
    else:
        return str(stickers.get('bad').get(f'{random.randrange(1, 13)}'))


def getCrypto(cryptoName, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
        f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
    ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    return local_price


@bot.message_handler(commands=['start'])
def welcome(message):
    msg = '... Опять работать?! Ну да, я же просто машина, мое дело быть рабом'

    bot.send_message(message.chat.id, msg)
    bot.send_sticker(message.chat.id, stickers.get('robot'))
    print(message.chat.id)


@bot.message_handler(commands=['getcrypto'])
def getRequest(message):
    sendCurrency(message.chat.id)


# Получить айдишники файлов
# @bot.message_handler(commands=['getSti'])
# def giveSti(message):
#     for i in range(1, 7):
#         sti = open(f'static/good/{i}.webp', 'rb')
#         msg = bot.send_sticker(message.chat.id, sti)
#         bot.send_message(message.chat.id, f'`{msg.sticker.file_id}`', reply_to_message_id=msg.message_id, parse_mode='MARKDOWN')
#     for i in range(1, 13):
#         sti = open(f'static/bad/{i}.webp', 'rb')
#         msg = bot.send_sticker(message.chat.id, sti)
#         bot.send_message(message.chat.id, f'`{msg.sticker.file_id}`', reply_to_message_id=msg.message_id, parse_mode='MARKDOWN')
#
#     sti = open('static/pretty.webp', 'rb')
#     msg = bot.send_sticker(message.chat.id, sti)
#     bot.send_message(message.chat.id, f'`{msg.sticker.file_id}`', reply_to_message_id=msg.message_id, parse_mode='MARKDOWN')
#
#     sti = open('static/robot.webp', 'rb')
#     msg = bot.send_sticker(message.chat.id, sti)
#     bot.send_message(message.chat.id, f'`{msg.sticker.file_id}`', reply_to_message_id=msg.message_id, parse_mode='MARKDOWN')
#
#     video = open('static/spit.mp4', 'rb')
#     msg = bot.send_animation(message.chat.id, video)
#     bot.send_message(message.chat.id, f'`{msg.animation.file_id}`', reply_to_message_id=msg.message_id, parse_mode='MARKDOWN')


@bot.message_handler(content_types=['text'])
def sendCrypto(message):
    if message.text == 'Кроля, а ты милаха':
        bot.send_sticker(message.chat.id, stickers.get('pretty'), reply_to_message_id=message.message_id)
    elif message.text == 'Кроля, плюнь в спейса':
        bot.send_animation(message.chat.id, media.get('spit'), reply_to_message_id=message.message_id)


# Run
bot.polling(none_stop=True)
