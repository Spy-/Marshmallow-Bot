import secrets

import discord
from marshmallow.core.utilities.constants import *

async def randombetween(cmd, message, args):
    if args:
        if len(args) == 2:
            try:
                min_num = int(args[0])
                max_num = int(args[1])
            except ValueError:
                min_num = None
                max_num = None
            if min_num and max_num:
                if max_num > min_num:
                    ran_num = secrets.randbelow(max_num - min_num)
                    out_num = min_num + ran_num
                    response = discord.Embed(color=0xea596e, title=f'🎲 {out_num}')
                else:
                    response = discord.Embed(color=ERROR, title='❗ The high number is smaller than the minimum.')
            else:
                response = discord.Embed(color=ERROR, title='❗ Invalid numbers.')
        else:
            response = discord.Embed(color=ERROR, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=ERROR, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)