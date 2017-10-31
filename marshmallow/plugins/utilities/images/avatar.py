import discord

from marshmallow.core.utilities.data_processing import get_image_colors
from marshmallow.core.utilities.data_processing import user_avatar


async def avatar(cmd, message, args):
    gif = False
    auto_color = False
    if args:
        if args[-1].lower() == 'gif':
            gif = True
        elif args[-1].lower() == 'auto':
            auto_color = True
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    ava_url = user_avatar(target, gif)
    if auto_color:
        color = await get_image_colors(ava_url)
    else:
        color = target.color
    embed = discord.Embed(color=color)
    if auto_color:
        embed.description = f'Dominant Color: #{str(hex(color)).split("x")[1].upper()}'
    embed.set_image(url=ava_url)
    await message.channel.send(None, embed=embed)