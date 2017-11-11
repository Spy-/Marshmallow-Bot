
import discord
from marshmallow.core.utilities.constants import *

async def deletecommands(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        curr_settings = cmd.db.get_guild_settings(message.guild.id, 'DeleteCommands')
        if curr_settings is None:
            curr_settings = False
        if curr_settings:
            cmd.db.set_guild_settings(message.guild.id, 'DeleteCommands', False)
            ending = 'disabled'
        else:
            cmd.db.set_guild_settings(message.guild.id, 'DeleteCommands', True)
            ending = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Command message deletion has been {ending}.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=ERROR)
    await message.channel.send(embed=response)