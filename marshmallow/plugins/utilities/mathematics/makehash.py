import hashlib

import discord
from marshmallow.core.utilities.constants import *

async def makehash(cmd, message, args):
    if not args:
        embed = discord.Embed(color=ERROR, title='❗ No hash inputted and nothing to hash.')
        await message.channel.send(None, embed=embed)
        return
    if len(args) < 2:
        embed = discord.Embed(color=ERROR, title='❗ Nothing to hash.')
        await message.channel.send(None, embed=embed)
        return
    hash_name = args[0]
    hashes = hashlib.algorithms_available
    if hash_name not in hashes:
        embed = discord.Embed(color=ERROR)
        embed.add_field(name='❗ Unknown Hashing Method',
                        value='Available:\n```\n' + ', '.join(hashes) + '\n```')
        await message.channel.send(None, embed=embed)
        return
    qry = ' '.join(args[1:])
    crypt = hashlib.new(hash_name)
    crypt.update(qry.encode('utf-8'))
    final = crypt.hexdigest()
    embed = discord.Embed(color=0x66cc66)
    embed.add_field(name=f'✅ Hashing With {hash_name.upper()} Done', value=f'```\n{final}\n```')
    await message.channel.send(None, embed=embed)