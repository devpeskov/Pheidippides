# Кроля бот. Дает крипту. Иногда не дает

Для запуска необходимо:
1. Скачать репо и установить зависимости:
```
git clone https://gitlab.com/freedom-pride-chat/crypto-kroleg.git
cd crypto-kroleg
# Разверните и активируйте венв если не хотите срать зависимостями
pip install -r requirements.txt
```
2. В корне проекта создать config.py со следующим содержимым:
```
# bot token from @BotFather
TOKEN = 'YOUR_BOT_TOKEN'
```
3. Заранить бота:
```
python bot.py
```

На этом все. Отрубить лютого можно комбинацией C-c.
