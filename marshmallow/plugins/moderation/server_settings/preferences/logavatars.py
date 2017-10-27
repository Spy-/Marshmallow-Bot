import discord


async def logavatars(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        log_edits = cmd.db.get_guild_settings(message.guild.id, 'LogAvatars')
        if log_edits:
            cmd.db.set_guild_settings(message.guild.id, 'LogAvatars', False)
            ender = 'disabled'
        else:
            cmd.db.set_guild_settings(message.guild.id, 'LogAvatars', True)
            ender = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Avatar change logging has been {ender}.')
    await message.channel.send(embed=response)