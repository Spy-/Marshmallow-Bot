import discord
import inspect

from marshmallow.core.utilities.constants import *


async def evaluate(cmd, message, args):
    if not args:
        status = discord.Embed(color=ERROR, title='❗ Nothing Inputted To Process')
    else:
        try:
            execution = " ".join(args)
            output = eval(execution)
            if inspect.isawaitable(output):
                output = await output
            status = discord.Embed(title='✅ Executed', color=0x77B255)
            status.add_field(name='Results', value=f'\n```\n{output}\n```')
        except Exception as e:
            status = discord.Embed(color=ERROR, title='❗ Error')
            status.add_field(name='Execution Failed', value=f'{e}')
    await message.channel.send(None, embed=status)