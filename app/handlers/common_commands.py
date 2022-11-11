from aiogram import Dispatcher, types  # type: ignore

from ..converter import convert_to_cmd_message
from ..crypto_api_service import get_all_coins, get_specific_coins
from ..static import chooseSticker


async def cmd_getcrypto(message: types.Message) -> None:
    coins = await get_specific_coins(["bitcoin", "ethereum", "monero"])
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)
    await message.answer_sticker(sticker_file_id)
    await message.answer(msg, parse_mode=types.ParseMode.HTML)


async def cmd_getallcoins(message: types.Message) -> None:
    coins = await get_all_coins()
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)
    await message.answer_sticker(sticker_file_id)
    await message.answer(msg, parse_mode=types.ParseMode.HTML)


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_getcrypto, commands="getcrypto")
    dp.register_message_handler(cmd_getallcoins, commands="getallcoins")
