"""
This file contains only 1 method: `fill_stickers`. The method uploads stickers
to telegram and returns their file_id and forms json-storge with them
"""
import json
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types  # type: ignore

from config import TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Usage of dispatcher:
# -----------------------------------------------------------------------------
@dp.message_handler(commands="fill_stickers")
async def send_stickers(message: types.Message):
    # percentage_list is needed to generate keys in json-storge
    percentage_list = [4, 8, 11, 15, 19, 23]
    file_id_dict = {}
    for i in range(1, 7):
        sti = open(f"webp_stickers/good/{i}.webp", "rb")
        msg = await message.answer_sticker(sti)
        await msg.reply(
            f"`{msg.sticker.file_id}`",
            parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        file_id_dict[f"positive{percentage_list[i-1]}"] = msg.sticker.file_id

    for i in range(1, 7):
        sti = open(f"webp_stickers/bad/{i}.webp", "rb")
        msg = await message.answer_sticker(sti)
        await msg.reply(
            f"`{msg.sticker.file_id}`",
            parse_mode=types.ParseMode.MARKDOWN_V2,
        )
        file_id_dict[f"negative{percentage_list[i-1]}"] = msg.sticker.file_id

    _jsonfile = Path(__file__).resolve().parent / "../app/mood_stickers.json"
    with open(_jsonfile, "w") as f:
        json.dump(file_id_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
