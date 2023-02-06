import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.config import TOKEN
from app.handlers.common_commands import register_handlers_common
from app.handlers.inline_mode import register_inline_handlers
from app.handlers.schedule_manager import register_schedule_manager
from app.schedule import scheduler

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="/start",
            description="introduction to the bot",
        ),
        BotCommand(
            command="/getcrypto",
            description="get a short list of cryptocurrency rates",
        ),
        BotCommand(
            command="/getallcoins",
            description="get extended list of cryptocurrency rates",
        ),
        BotCommand(
            command="/subscribe",
            description="subscribe to daily cryptocurrency rate",
        ),
        BotCommand(
            command="/unsubscribe",
            description="unsubscribe to daily cryptocurrency rate",
        ),
    ]
    await bot.set_my_commands(commands)


async def del_commands(bot: Bot) -> None:
    await bot.delete_my_commands()


async def main() -> None:
    # Setting logging to stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    register_handlers_common(dp)
    register_inline_handlers(dp)
    register_schedule_manager(dp)

    # await del_commands(bot)
    await set_commands(bot)

    asyncio.get_event_loop().create_task(scheduler())

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
