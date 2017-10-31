import secrets
import discord

async def coinflip(cmd, message, args):
    result = secrets.choice(['heads', 'tails'])
    urls = {
        'heads': 'https://i.imgur.com/528MDba.png',
        'tails': 'https://i.imgur.com/A42nfrB.png'
    }
    embed = discord.Embed(color=0x1abc9c)
    if args:
        choice = args[0]
        if choice.lower().startswith('t') or choice.lower().startswith('h'):
            if choice.lower().startswith('t'):
                choice = 'tails'
            else:
                choice = 'heads'
            if result == choice.lower():
                out = '☑ Nice guess!'
            else:
                out = '🇽 Better luck next time!'
            embed = discord.Embed(color=0x1abc9c, title=out)
    embed.set_image(url=urls[result])
    await message.channel.send(None, embed=embed)