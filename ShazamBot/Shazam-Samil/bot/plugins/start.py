from bot import bot
from pyrogram import filters


@bot.on_message(
    filters.command("start")
)
async def alive(_, message):
    await message.reply(
        f"Salam {message.from_user.mention}, Bu qeyri -rəsmi Telegram Shazam Botudur.\n\nℹ️ Mənə bir səs, video və ya səsli not göndərə bilərsiniz ki, Shazam -ı təhlil edim və nəticələri sizə göndərim."
    )