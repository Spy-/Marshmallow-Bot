import discord

from marshmallow.core.utilities.constants import *

async def playlist(cmd, message, args):

    if len(args) >= 1:
        if args[0].lower() == 'create':
            create(cmd, message, args[1:])
        elif args[0].lower() == 'remove':
            remove(cmd, message, args[1:])
        elif args[0].lower() == 'play':
            play(cmd, message, args[1:])
        elif args[0].lower() == 'edit':
            edit(cmd, message, args[1:])
    else:
        response = 'You must pass a subcommand: `create`, `remove`, `play`, `edit`'
        await message.channel.send(response)


def create(cmd, message, args):
    author = message.author
    bot = cmd.bot
    db = cmd.db
    playlists = cmd.db.get_playlists(author)

    if args[0]:
        name = args[0]
        db.insert_playlist(author, name)
        response = discord.Embed(color=EXECUTE_GREEN, title=f'Playlist: {name} successfully created.')
    else:
        response = discord.Embed(color=ERROR, title='You must give the playlist a name')


def remove(cmd, message, args):
    author = message.author
    bot = cmd.bot
    db = cmd.db


def play(cmd, message, args):
    author = message.author
    bot = cmd.bot
    db = cmd.db


def edit(cmd, message, args):
    author = message.author
    bot = cmd.bot
    db = cmd.db
