from aiogram import Dispatcher, types  # type: ignore

from ..crypto_api_service import Coin, get_coin


async def cmd_getcrypto(message: types.Message) -> None:
    msg = "The current course is this:\n"
    for coin_id in ["bitcoin", "ethereum", "monero"]:
        coin = await get_coin(coin_id)
        msg += _form_msg(coin)
    await message.answer(msg)


def _form_msg(coin: Coin):
    return f"\n{coin.name}: {coin.price} ({coin.price_change_24h:+})"


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_getcrypto, commands="getcrypto")
