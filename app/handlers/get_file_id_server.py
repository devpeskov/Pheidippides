# Получить айдишники файлов
# @bot.message_handler(commands=["getSti"])
# def giveSti(message):
#     for i in range(1, 7):
#         sti = open(f"static/good/{i}.webp", "rb")
#         msg = bot.send_sticker(message.chat.id, sti)
#         bot.send_message(
#             message.chat.id,
#             f"`{msg.sticker.file_id}`",
#             reply_to_message_id=msg.message_id,
#             parse_mode="MARKDOWN",
#         )
#     for i in range(1, 13):
#         sti = open(f"static/bad/{i}.webp", "rb")
#         msg = bot.send_sticker(message.chat.id, sti)
#         bot.send_message(
#             message.chat.id,
#             f"`{msg.sticker.file_id}`",
#             reply_to_message_id=msg.message_id,
#             parse_mode="MARKDOWN",
#         )
#
#     sti = open("static/pretty.webp", "rb")
#     msg = bot.send_sticker(message.chat.id, sti)
#     bot.send_message(
#         message.chat.id,
#         f"`{msg.sticker.file_id}`",
#         reply_to_message_id=msg.message_id,
#         parse_mode="MARKDOWN",
#     )
#
#     sti = open("static/robot.webp", "rb")
#     msg = bot.send_sticker(message.chat.id, sti)
#     bot.send_message(
#         message.chat.id,
#         f"`{msg.sticker.file_id}`",
#         reply_to_message_id=msg.message_id,
#         parse_mode="MARKDOWN",
#     )
#
#     video = open("static/spit.mp4", "rb")
#     msg = bot.send_animation(message.chat.id, video)
#     bot.send_message(
#         message.chat.id,
#         f"`{msg.animation.file_id}`",
#         reply_to_message_id=msg.message_id,
#         parse_mode="MARKDOWN",
#     )
