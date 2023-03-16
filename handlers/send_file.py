# (c) @AbirHasan2005 | @PredatorHackerzZ

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64


async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"**Here is Sharable Link of this File:**\n"
            f"<a href=https://telegram.dog/{Config.BOT_USERNAME}?start=tgnvs_{str_to_b64(str(file_id))}>DOWNLOAD LINK 🔗</a>\n\n"
            f"__To Retrive the Stored File, just open the link!__",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
				[
                    [InlineKeyboardButton("🎬 𝙼𝚘𝚟𝚒𝚎 Link Channal 🎬", url="https://t.me/+O0aUO3TbgR8xZjNl")]
                ]
			)
            quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)


async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)


async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
    await asyncio.sleep(2)
