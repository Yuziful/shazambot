from pyrogram import types, filters
from bot import bot


@bot.on_inline_query()
async def inline_func(client, query):
    string = query.query.lower()
    answers = []
    if string == '':
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text='Köməyə ehiyacın var? onda bura vur',
            switch_pm_parameter='help_inline',
        )
        return
    if string.split()[0] == 'related':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Mahnı ID -ni daxil edin',
                switch_pm_parameter='help_inline',
            )
            return
        try:
            track_id = int(string.split(None, 1)[1])
        except ValueError:
            return
        try:
            for x in (await bot.related(track_id)):
                try:
                    result = (
                        x['images']['coverarthq'],
                        x['images']['coverart'],
                        x['title'], x['subtitle'],
                        x['share']['href'],
                        x['share']['html']
                    )
                except KeyError:
                    result = (
                        None,
                        None,
                        x['title'],
                        x['subtitle'],
                        x['share']['href'],
                        x['share']['html']
                    )
                image, thumb, title, artist, link, share = result
                answers.append(
                    types.InlineQueryResultArticle(
                        title=title,
                        description=artist,
                        thumb_url=thumb,
                        input_message_content=types.InputTextMessageContent(
                            f'**Başlıq**: {title}\n**Müğənni**: {artist}[\u200c\u200c\u200e]({image})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🔗 Paylaş',
                                        url=f'{share}'
                                    )
                                ],
                                [
                                    types.InlineKeyboardButton(
                                        '🎵 Dinlə',
                                        url=f'{link}'
                                    )
                                ]
                            ]
                        )
                    )
                )
        except TypeError:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Mahnini tapa bilmirem',
                switch_pm_parameter='help_inline',
            )
            return
    elif string.split()[0] == 'artist':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Sənətçinin adını daxil edin',
                switch_pm_parameter='help_inline',
            )
            return
        artists = await bot.get_artist(string.split(None, 1)[1])
        if artists is None:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Sənətçi tapılmadı',
                switch_pm_parameter='help_inline',
            )
            return
        for artist in artists:
            answers.append(
                types.InlineQueryResultArticle(
                        title=artist.name,
                        description=None,
                        thumb_url=artist.avatar or None,
                        input_message_content=types.InputTextMessageContent(
                            f'**Müğənni Adı:**{artist.name} [\u200c\u200c\u200e]({artist.avatar})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🔗 Daha çox məlumat',
                                        url=f'{artist.url}'
                                    )
                                ]
                            ]
                        )
                    ) 
                )
    elif string.split()[0] == 'tracks':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Müğənni kimliyini daxil edin',
                switch_pm_parameter='help_inline',
            )
            return
        tracks = await bot.get_artist_tracks(string.split(None, 1)[1])
        if tracks is None:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Sənətçi tapılmadı',
                switch_pm_parameter='help_inline',
            )
            return
        for track in tracks:
            answers.append(
                types.InlineQueryResultArticle(
                        title=track.title,
                        description=track.subtitle,
                        thumb_url=track.apple_music_url or None,
                        input_message_content=types.InputTextMessageContent(
                            f'**Başlıq:** {track.title}\n**Müğənni**: {track.subtitle} [\u200c\u200c\u200e]({track.apple_music_url})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🎵 Dinlə',
                                        url=f'{track.shazam_url}'
                                    )
                                ]
                            ]
                        )
                    ) 
                )
    await client.answer_inline_query(
        query.id,
        results=answers,
        cache_time=0,
    )
