from bot import bot, max_file


from pyrogram import filters, types
import os


@bot.on_message(filters.audio | filters.video | filters.voice)
async def voice_handler(_, message):
    file_size = message.audio or message.video or message.voice
    if max_file < file_size.file_size :
        await message.reply_text(
            "**⚠️ Maksimum fayl ölçüsünə çatıldı.**"
        )
        return
    file = await message.download(f'{bot.rnd_id()}.mp3')
    r = (await bot.recognize(file)).get('track', None)
    os.remove(file)
    if r is None:
        await message.reply_text(
            '**⚠️ Səsi tanımaq olmur**'
        )
        return
    out = f'**Başlıq**: `{r["title"]}`\n'
    out += f'**Müğənni**: `{r["subtitle"]}`\n'
    buttons = [
            [
                types.InlineKeyboardButton(
                    '🎼 Əlaqəli mahnılar',
                    switch_inline_query_current_chat=f'related {r["key"]}',
                ),
                types.InlineKeyboardButton(
                    '🔗 Paylaş',
                    url=f'{r["share"]["html"]}'
                )
            ],
            [
                types.InlineKeyboardButton(
                    '🎵 Dinlə',
                    url=f'{r["url"]}'
                )
            ],        
        ]
    response = r.get('artists', None)
    if response:
        buttons.append(
            [
                types.InlineKeyboardButton(
                    f'💿 {r["subtitle"]} - dən daha çox musiqi',
                    switch_inline_query_current_chat=f'Musiqi {r["artists"][0]["id"]}',
                )
            ]
        )
    await message.reply_photo(
        r['images']['coverarthq'],
        caption=out,
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )