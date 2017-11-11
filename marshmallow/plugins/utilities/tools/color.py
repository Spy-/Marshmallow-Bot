import os
import discord
from PIL import Image
from marshmallow.core.utilities.constants import *

async def color(cmd, message, args):
    if args:
        if len(args) == 1:
            color_input = args[0]
            while color_input.startswith('#'):
                color_input = color_input[1:]
            while color_input.startswith('0x'):
                color_input = color_input[2:]
            if len(color_input) == 6:
                try:
                    color_tupple = (int(color_input[:2], 16), int(color_input[2:-2], 16), int(color_input[4:], 16))
                    response = None
                    image = Image.new('RGB', (128, 128), color_tupple)
                    image.save(f'cache/{message.id}.png')
                except ValueError:
                    response = discord.Embed(color=ERROR, title='❗ Something here is not a number.')
            else:
                response = discord.Embed(color=ERROR, title='❗ Invalid HEX color code.')
        elif len(args) == 3:
            try:
                color_tupple = (int(args[0]), int(args[1]), int(args[2]))
                response = None
                image = Image.new('RGB', (128, 128), color_tupple)
                image.save(f'cache/{message.id}.png')
            except ValueError:
                response = discord.Embed(color=ERROR, title='❗ Something here is not a number.')
        else:
            response = discord.Embed(color=ERROR, title='❗ Invalid input, HEX or RGB sequence, please.')
    else:
        response = discord.Embed(color=ERROR, title='❗ Nothing inputted.')
    if response:
        await message.channel.send(embed=response)
    else:
        img_file = discord.File(f'cache/{message.id}.png')
        await message.channel.send(file=img_file)
        os.remove(f'cache/{message.id}.png')