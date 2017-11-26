import discord
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from marshmallow.core.utilities.constants import *


async def evaluate(cmd, message, args):
    env = {
        'bot': cmd.bot,
        'channel': message.channel,
        'author': message.author,
        'guild': message.guild,
        'message': message,
        'args': args,
        'cmd': cmd
    }

    env.update(globals())

    stdout = io.StringIO()

    body = " ".join(args)

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await message.channel.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await message.channel.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await message.channel.message.add_reaction('\u2705')
        except:
            pass
        if ret is None:
            if value:
                await message.channel.send(f'```py\n{value}\n```')
