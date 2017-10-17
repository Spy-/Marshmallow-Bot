from discord.ext import commands
import discord.utils
from .config import Config, ConfigDefaults

config = Config(ConfigDefaults.options_file)

def is_owner_check(ctx):
    return ctx.message.author.id == 203297462746611712


def is_owner():
    return commands.check(is_owner_check)

''' def check_permissions(ctx, perms):
    if is_owner_check(ctx):
        return True
    elif not perms:
        return False

    ch = ctx.message.channel
    author = ctx.message.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items()) '''

def check_permissions(**perms):
    def predicate(ctx):
        # Return true if this is a private channel, we'll handle that in the registering of the command
        if type(ctx.message.channel) is discord.DMChannel:
            return True

        # Get the member permissions so that we can compare
        guild_perms = ctx.message.author.guild_permissions
        channel_perms = ctx.message.author.permissions_in(ctx.message.channel)
        # Currently the library doesn't handle administrator overrides..so lets do this manually
        if guild_perms.administrator:
            return True
        # Next, set the default permissions if one is not used, based on what was passed
        # This will be overriden later, if we have custom permissions
        required_perm = discord.Permissions.none()
        for perm, setting in perms.items():
            setattr(required_perm, perm, setting)

        required_perm_value = ctx.bot.db.load('server_settings', key=ctx.message.guild.id, pluck='permissions') or {}
        required_perm_value = required_perm_value.get(ctx.command.qualified_name)
        if required_perm_value:
            required_perm = discord.Permissions(required_perm_value)

        # Now just check if the person running the command has these permissions
        return guild_perms >= required_perm or channel_perms >= required_perm

    predicate.perms = perms
    return commands.check(predicate)


def role_or_permissions(ctx, check, **perms):
    if check_permissions(**perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def mod_or_permissions(**perms):
    def predicate(ctx):
        server = ctx.message.server
        mod_role = config.mod_role.lower()
        admin_role = config.admin_role.lower()
        return role_or_permissions(ctx, lambda r: r.name.lower() in (mod_role, admin_role), **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        server = ctx.message.server
        admin_role = config.admin_role
        return role_or_permissions(ctx, lambda r: r.name.lower() == admin_role.lower(), **perms)

    return commands.check(predicate)


def serverowner_or_permissions(**perms):
    def predicate(ctx):
        if ctx.message.server is None:
            return False
        server = ctx.message.server
        owner = server.owner

        if ctx.message.author.id == owner.id:
            return True

        return check_permissions(**perms)
    return commands.check(predicate)


def serverowner():
    return serverowner_or_permissions()


def admin():
    return admin_or_permissions()


def mod():
    return mod_or_permissions()