import asyncio
import logging

from aiogram import Bot, Dispatcher  # type: ignore
from aiogram.types import BotCommand  # type: ignore

from app.handlers.common_commands import register_handlers_common
from app.config import TOKEN

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="/getcrypto",
            description="Get a cryptocurrency rate",
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

    # await del_commands(bot)
    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
