from aiogram import Dispatcher, types

from ..chat_storage import ChatStorage


async def subscribe(message: types.Message) -> None:
    chat_storage = ChatStorage()
    is_result_success = chat_storage.add_chat(message.chat.id)

    if is_result_success:
        msg = "Subscription completed!"
    else:
        msg = "Subscription is already activated."
    msg = "\n\n".join([msg, "You can unsubscribe with command: /unsubscribe"])
    await message.answer(msg, parse_mode=types.ParseMode.HTML)


async def unsubscribe(message: types.Message) -> None:
    chat_storage = ChatStorage()
    is_result_success = chat_storage.remove_chat(message.chat.id)

    if is_result_success:
        msg = "Subscription canceled!"
    else:
        msg = "This chat is not subscribed to daily cryptocurrency rate."
    msg = "\n\n".join([msg, "You can subscribe with command: /subscribe"])

    await message.answer(msg, parse_mode=types.ParseMode.HTML)


def register_schedule_manager(dp: Dispatcher) -> None:
    dp.register_message_handler(subscribe, commands="subscribe")
    dp.register_message_handler(unsubscribe, commands="unsubscribe")
