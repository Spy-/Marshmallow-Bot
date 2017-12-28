import discord

from marshmallow.core.utilities.data_processing import user_avatar
from marshmallow.core.utilities.constants import *

async def skip(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                queue = cmd.bot.music.get_queue(message.guild.id)
                if queue:
                    curr = cmd.bot.music.currents[message.guild.id]
                    message.guild.voice_client.stop()
                    response = discord.Embed(color=0x66CC66, title=f'✅ Skipping {curr.title}.')
                    requester = f'{message.author.name}#{message.author.discriminator}'
                    response.set_author(name=requester, icon_url=user_avatar(message.author))
                else:
                    response = discord.Embed(color=ERROR, title='❗ The queue is empty or this is the last song.')
            else:
                response = discord.Embed(color=ERROR, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=ERROR, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=ERROR, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)