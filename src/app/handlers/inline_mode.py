from aiogram import Dispatcher, types  # type: ignore

from ..converter import (
    convert_to_inline_description,
    convert_to_input_msg_content,
)
from ..crypto_api_service import get_all_coins
from ..objects import Coin


async def inline_handler(query: types.InlineQuery) -> None:
    results = []
    coins = _filter_coins(await get_all_coins(), query.query)
    for coin in coins:
        results.append(
            types.InlineQueryResultArticle(
                id=coin.id,
                title=coin.name,
                description=convert_to_inline_description(coin),
                input_message_content=convert_to_input_msg_content(coin),
                thumb_url=coin.img_small,
            )
        )
    await query.answer(
        results=results,
        cache_time=30,
        is_personal=False,
    )


def _filter_coins(coins: list[Coin], filter_msg: str) -> list[Coin]:
    if not filter_msg:
        return coins
    else:
        sorted_coins = []
        for coin in coins:
            if (
                filter_msg.lower() in coin.name.lower()
                or filter_msg.lower() in coin.id.lower()
                or filter_msg.lower() in coin.symbol.lower()
            ):
                sorted_coins.append(coin)
        return sorted_coins


def register_inline_handlers(dp: Dispatcher) -> None:
    dp.register_inline_handler(inline_handler)
