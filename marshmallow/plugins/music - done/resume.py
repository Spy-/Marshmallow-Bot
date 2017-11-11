import discord
from marshmallow.core.utilities.constants import *

async def resume(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                if message.guild.voice_client.is_paused():
                    message.guild.voice_client.resume()
                    response = discord.Embed(color=0x3B88C3, title=f'⏯ Music has been resumed.')
                else:
                    response = discord.Embed(color=ERROR, title='❗ The player is not paused.')
            else:
                response = discord.Embed(color=ERROR, title='❗ I am not connected to a voice channel.')
        else:
            response = discord.Embed(color=ERROR, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=ERROR, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)