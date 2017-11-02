import discord
import asyncio


async def volume(cmd, message, args):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if args:
                _volume = int(args[0])
                if _volume > 0:
                    if _volume < 200:
                        cmd.bot.music.set_volume(message.guild.id, _volume / 100)
                        response = discord.Embed(color=0x66CC66, title=f'✅ Volume changed to {_volume}%')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ Volume must be below 200.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Volume must be above 0.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')

    #response = discord.Embed(color = 0xBE1931, title='❗ This hasnt been implemented yet. #TODO')    
    await message.channel.send(embed=response)