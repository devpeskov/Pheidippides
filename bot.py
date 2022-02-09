import telebot
import config
import requests
from decimal import Decimal
import schedule
import time

bot = telebot.TeleBot(config.TOKEN)


def sendCurrency():
    msg = f'Ныне курса таков:\n\nБиток биток биточек: {getCrypto("bitcoin")}' \
              f'\nБутырка: {getCrypto("ethereum")}\n' \
              f'Нидзямонета: {getCrypto("monero")}\n'
    sti = open('static/all.webp', 'rb')
    bot.send_sticker('-1001691787586', sti)
    bot.send_message('-1001691787586', msg)


def getCrypto(cryptoName, baseCurrency='usd'):
    '''Parses json response and outputs value to polybar'''
    json = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cryptoName}',
            ).json()["market_data"]
    local_price = round(Decimal(json["current_price"][f'{baseCurrency}']), 2)
    return local_price


# schedule.every(10).seconds.do(sendCurrency)
schedule.every(10).minutes.do(sendCurrency)
# schedule.every().hour.do(sendCurrency)
# schedule.every().day.at("10:30").do(sendCurrency)
# schedule.every(5).to(10).minutes.do(sendCurrency)
# schedule.every().monday.do(sendCurrency)
# schedule.every().wednesday.at("13:15").do(sendCurrency)
# schedule.every().minute.at(":17").do(sendCurrency)

while True:
    schedule.run_pending()
    time.sleep(1)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/robot.webp', 'rb')
    bot.send_message(message.chat.id, 'Блять... Еще больше работы?!')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Ну типа хер я тебе команды вывалю')
    print(message.chat.id)


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


# Run
bot.polling(none_stop=True)
