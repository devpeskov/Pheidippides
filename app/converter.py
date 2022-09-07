from aiogram import types  # type: ignore

from .crypto_api_service import Coin


def convert_to_cmd_message(coins: list[Coin]) -> str:
    msg = "The current course is this:\n"
    for coin in coins:
        msg += (
            f"\n<b>{coin.name}</b>: ${coin.price} ({coin.price_change_24h:+}%)"
        )
    return msg


def convert_to_inline_description(coin: Coin) -> str:
    return f"{coin.name}: ${coin.price} ({coin.price_change_24h:+}%)"


def convert_to_input_msg_content(coin: Coin) -> types.InputTextMessageContent:
    return types.InputTextMessageContent(
        f"<b>{coin.name}</b>: ${coin.price} ({coin.price_change_24h:+}%)",
        parse_mode=types.ParseMode.HTML,
    )
