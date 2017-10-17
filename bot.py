from collections import Counter
import traceback
import datetime
import logging
import asyncio
import copy
import json
import sys
import os

from discord.ext import commands
import discord
from cogs import utils

os.chdir(os.path.dirname(os.path.realpath(__file__)))


discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='marshmallow.log', encoding='utf-8', mode='w')
log.addHandler(handler)


config = utils.Config(utils.ConfigDefaults.options_file)

extensions = [
    'cogs.dj',
    'cogs.meta',
    'cogs.misc',
    'cogs.owner',
    'cogs.music'
    #'cogs.playlist',
]

opts = {'command_prefix': config.command_prefix,
        'description': config.description,
        'pm_help': True,
        'help_attrs': dict(hidden=True),
        'formatter': commands.HelpFormatter(show_check_failure=True),
        'game': discord.Game(name=config.default_status, type=0)}

bot = commands.Bot(**opts)


def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)


@bot.event
async def on_member_join(member):
    guild = member.guild
    messages = load_messages()
    guildstr = str(guild.id)
    if guildstr not in messages:
        return
    if 'welcome' not in messages[guildstr]:
        return
    srv = messages[guildstr]
    chanid = srv['channel']
    channel = bot.get_channel(chanid)
    wlc = messages[guildstr]['welcome'].format(member)
    await channel.send(wlc)


@bot.event
async def on_ready():
    print('------------------------------------')
    print('Marshmallow is logged in and online!')
    print("discord.py version is " + discord.__version__)
    print('------------------------------------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()


@bot.event
async def on_member_ban(guild, user):
    for channel in guild.channels:
        if channel.name == "banlogs":
            await channel.send("**BAN** \n**User**: {0}".format(user))
            break


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    author = ctx.message.author
    ignored = (commands.CommandNotFound, commands.UserInputError)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
        return
    elif isinstance(error, commands.NoPrivateMessage):
        await discord.User.trigger_typing(author)
        await asyncio.sleep(1)
        await author.send("Um... this command can't be used in dms.")
    elif isinstance(error, commands.DisabledCommand):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send("I'm Sorry. This command is disabled and it can't be used.")
    elif isinstance(error, commands.CommandInvokeError):
        channel = ctx.message.channel
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(
            error.original), file=sys.stderr)
        e = discord.Embed(title='Inkx! I have encountered an Error!', color=0xcc6600)
        e.add_field(name='Invoke', value=error)
        e.description = '```py\nIn {0.command.qualified_name}:\n```'.format(
            ctx) + '{0.__class__.__name__}: {0}'.format(error.original)
        e.timestamp = datetime.datetime.utcnow()
        ch = bot.get_channel(369544513565229066)
        try:
            await ch.send(embed=e)
        except:
            pass

    elif isinstance(error, commands.CommandNotFound):
        log.info(f"\"{ctx.message.guild}\": \"{ctx.message.author}\" used a command thats not in Inkxbot, content is resent here: '{ctx.message.content}'")
    elif isinstance(error, commands.MissingRequiredArgument):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send(f"You've asked me about my `{ctx.command}` command without arguments, use `,help {ctx.command}`")


@bot.event
async def on_error(event, *args, **kwargs):
    e = discord.Embed(title='Zoinks! I have encountered an Error!', color=0xcc6600)
    e.add_field(name='Event', value=event)
    e.description = f'```py\n{traceback.format_exc()}\n```'
    e.timestamp = datetime.datetime.utcnow()
    ch = bot.get_channel(369544513565229066)
    try:
        log.info(event)
        await ch.send(embed=e)
    except:
        pass


@bot.event
async def on_resumed():
    print('resumed...')


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


if __name__ == '__main__':
    bot.commands_used = Counter()
    bot.remove_command('help')
    print('------------------------------------')
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {} extension.'.format(extension))
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(config.token)
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
