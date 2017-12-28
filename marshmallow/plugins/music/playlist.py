import discord

from marshmallow.core.mechanics.database import Database

async def playlist(cmd, message, args):

    if args:
        subcommand = args[0].lower()

    if subcommand:
        args = args[1:]

    if subcommand == 'list':
        await _list(cmd, message, args)
    elif subcommand == 'create':
        await _create(cmd, message, args)


async def _list(cmd, message, args):
    await message.channel.send(args)

async def _create(cmd, message, args):
    if args:
        if args[0]:
            playlist_name = args[0]
        if args[1]:
            playlist_url = args[1]

        playlist = {
            'name': playlist_name,
            'url': playlist_url
        }

    
    
    await message.channel.send(args)