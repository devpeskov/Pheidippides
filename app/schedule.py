import asyncio

import aioschedule  # type: ignore
from aiogram import Bot, types  # type: ignore

from .config import CHAT_ID, TOKEN
from .converter import convert_to_cmd_message
from .crypto_api_service import get_specific_coins
from .static import chooseSticker


async def cmd_getcrypto() -> None:
    bot = Bot(token=TOKEN)
    coins = await get_specific_coins(["bitcoin", "ethereum", "monero"])
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)
    await bot.send_sticker(chat_id=CHAT_ID, sticker=sticker_file_id)
    await bot.send_message(
        chat_id=CHAT_ID, text=msg, parse_mode=types.ParseMode.HTML
    )


async def scheduler():
    aioschedule.every().day.at("06:00").do(cmd_getcrypto)
    aioschedule.every().day.at("18:00").do(cmd_getcrypto)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)
