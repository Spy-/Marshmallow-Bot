import discord
import secrets
from marshmallow.core.utilities.data_processing import user_avatar


async def shuffle(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                queue = cmd.bot.music.get_queue(message.guild.id)
                if queue:
                    new_queue = []
                    while queue:
                        new_queue.append(queue.pop(secrets.randbelow(len(queue))))
                    cmd.bot.music.queues.update({message.guild.id: new_queue})
                    response = discord.Embed(color=0x3B88C3, title=f'🔀 Shuffled {len(new_queue)} songs.')
                    requester = f'{message.author.name}#{message.author.discriminator}'
                    response.set_author(name=requester, icon_url=user_avatar(message.author))
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The queue is empty.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)