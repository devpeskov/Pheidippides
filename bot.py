import telebot
import config
import requests
from decimal import Decimal

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/robot.webp', 'rb')
    bot.send_message(message.chat.id, 'Блять... Еще больше работы?!')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Ну типа хер я тебе команды вывалю')

@bot.message_handler(content_types=['text'])
def sendCrypto(message):
    if message.text == 'Кроля, дай монетку':
        msg = f'Ну держи.\n\nБиток биток биточек: {getCrytpo("bitcoin")}\n'
        sti = open('static/btc.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, msg)
    elif message.text == 'Кроля, дай многа монеток':
        msg = f'Ох... Ладно\n\nБиток биток биточек: {getCrytpo("bitcoin")}\n' \
                  f'Бутырка: {getCrytpo("ethereum")}\n' \
                  f'Нидзямонета: {getCrytpo("monero")}\n'
        sti = open('static/all.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, msg)
    elif message.text == 'Кроля, что скажешь?':
        sti = open('static/n.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    elif message.text == 'Кроля, а ты милаха':
        sti = open('static/pretty.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    else:
        sti = open('static/angry.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, 'Чувак, серьезно, отьебись а. \
Все вопросы к спейсу. Ес чо он бота не сделал, \
у Юрца уже все готово')


def getCrytpo(cryptoName, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
            ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    return local_price


# Run
bot.polling(none_stop=True)
