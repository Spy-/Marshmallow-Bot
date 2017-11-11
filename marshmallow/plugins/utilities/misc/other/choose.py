import secrets

import discord
from marshmallow.core.utilities.constants import *

async def choose(cmd, message, args):
    if args:
        choice = secrets.choice(' '.join(args).split(' '))
        response = discord.Embed(color=0x1ABC9C, title='🤔 I choose... ' + choice)
    else:
        response = discord.Embed(color=ERROR, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)