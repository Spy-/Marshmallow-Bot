import discord

async def playlists(cmd, message, args):
    author = message.author
    bot = cmd.bot
    db = cmd.db
    playlists = db.get_playlists(author)
    await message.channel.send(playlists)