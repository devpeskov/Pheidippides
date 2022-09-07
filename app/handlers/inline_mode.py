from aiogram import Dispatcher, types  # type: ignore

from ..converter import (
    convert_to_inline_description,
    convert_to_input_msg_content,
)
from ..crypto_api_service import get_all_coins


async def inline_handler(query: types.InlineQuery) -> None:
    results = []
    coins = await get_all_coins()
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
        cache_time=60,
        is_personal=False,
    )


def register_inline_handlers(dp: Dispatcher) -> None:
    dp.register_inline_handler(inline_handler)
