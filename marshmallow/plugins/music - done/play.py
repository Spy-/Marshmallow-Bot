import discord
import asyncio
import datetime
from marshmallow.core.utilities.data_processing import user_avatar
from marshmallow.core.utilities.stats_processing import add_special_stats


async def play(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if args:
                await cmd.bot.modules.commands['queue'].execute(message, args)
            queue = cmd.bot.music.get_queue(message.guild.id)
            if queue:
                if not message.guild.voice_client:
                    await cmd.bot.modules.commands['summon'].execute(message, args)
                while cmd.bot.music.get_queue(message.guild.id):
                    if not message.guild.voice_client:
                        return
                    item = cmd.bot.music.queue_get(message.guild.id)
                    if message.guild.id in cmd.bot.music.repeaters:
                        cmd.bot.music.queue_add(
                            message.guild.id, item.requester, item.item_info)
                    if message.guild.voice_client.is_playing():
                        return
                    init_song_embed = discord.Embed(
                        color=0x3B88C3, title=f'🔽 Downloading {item.title}...')
                    init_song_msg = await message.channel.send(embed=init_song_embed)
                    await item.create_player(message.guild.voice_client)
                    await add_special_stats(cmd.db, 'songs_played')
                    cmd.bot.music.currents.update({message.guild.id: item})
                    duration = str(datetime.timedelta(seconds=item.duration))
                    author = f'{item.requester.name}#{item.requester.discriminator}'
                    song_embed = discord.Embed(color=0x3B88C3)
                    song_embed.add_field(
                        name='🎵 Now Playing', value=item.title)
                    song_embed.set_thumbnail(url=item.thumbnail)
                    song_embed.set_author(name=author, icon_url=user_avatar(
                        item.requester), url=item.url)
                    song_embed.set_footer(text=f'Duration: {duration}')
                    await init_song_msg.edit(embed=song_embed)
                    while message.guild.voice_client and message.guild.voice_client.is_playing():
                        await asyncio.sleep(2)
                response = discord.Embed(
                    color=0x3B88C3, title='🎵 Queue complete.')
                if message.guild.voice_client:
                    await message.guild.voice_client.disconnect()
                    if message.guild.id in cmd.bot.music.queues:
                        cmd.bot.music.queues.update({message.guild.id: []})
                #await cmd.bot.modules.commands['donate'].execute(message, ['mini'])
            else:
                response = discord.Embed(
                    color=0xBE1931, title='❗ The queue is empty.')
        else:
            response = discord.Embed(
                color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(
            color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)
