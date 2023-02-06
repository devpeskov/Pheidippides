import asyncio
import logging

import aioschedule
from aiogram import Bot, types
from aiogram.utils.exceptions import BadRequest, BotBlocked, BotKicked

from .chat_storage import ChatStorage
from .config import TOKEN
from .converter import convert_to_cmd_message
from .crypto_api_service import get_specific_coins
from .static import chooseSticker


async def cmd_getcrypto() -> None:
    bot = Bot(token=TOKEN)
    coins = await get_specific_coins(["bitcoin", "ethereum", "monero"])
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)

    chat_storage = ChatStorage()
    for chat_id in chat_storage.get_list_of_chats():
        try:
            await bot.send_sticker(chat_id=chat_id, sticker=sticker_file_id)
            await bot.send_message(
                chat_id=chat_id, text=msg, parse_mode=types.ParseMode.HTML
            )
        except BotKicked as e:
            logging.error(e, f"chat_id: {chat_id}")
            chat_storage.remove_chat(chat_id)
        except BotBlocked as e:
            logging.error(e, f"chat_id: {chat_id}")
            chat_storage.remove_chat(chat_id)
        except BadRequest as e:
            logging.error(e, chat_id)
        except Exception as e:
            logging.error(e, chat_id)


async def scheduler():
    aioschedule.every().day.at("06:00").do(cmd_getcrypto)
    aioschedule.every().day.at("18:00").do(cmd_getcrypto)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)
