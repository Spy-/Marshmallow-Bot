import discord


async def userid(cmd, message, args):
    embed = True
    if args:
        if args[-1].lower() == 'text':
            embed = False
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    response = discord.Embed(color=0x3B88C3)
    response.add_field(name=f'ℹ {target.name}', value=f'`{target.id}`')
    if embed:
        await message.channel.send(embed=response)
    else:
        await message.channel.send(target.id)