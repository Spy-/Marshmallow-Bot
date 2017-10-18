from discord.ext import commands
import discord.utils
from .config import Config, ConfigDefaults
import rethinkdb as r

config = Config(ConfigDefaults.options_file)

# The tables needed for the database, as well as their primary keys
required_tables = {
    'battle_records': 'member_id',
    'boops': 'member_id',
    'command_usage': 'command',
    'overwatch': 'member_id',
    'picarto': 'member_id',
    'server_settings': 'server_id',
    'raffles': 'server_id',
    'strawpolls': 'server_id',
    'osu': 'member_id',
    'tags': 'server_id',
    'tictactoe': 'member_id',
    'twitch': 'member_id',
    'user_playlists': 'member_id',
    'birthdays': 'member_id'
}


async def db_check():
    """Used to check if the required database/tables are setup"""
    db_opts = {'host': "127.0.0.1", 'db': "JohnPC_rqx", 'port': 28015} #, 'user': db_user, 'password': db_pass}

    r.set_loop_type('asyncio')
    # First try to connect, and see if the correct information was provided
    try:
        conn = await r.connect(**db_opts)
    except r.errors.ReqlDriverError:
        print("Cannot connect to the RethinkDB instance with the following information: {}".format(db_opts))

        print("The RethinkDB instance you have setup may be down, otherwise please ensure you setup a"
              " RethinkDB instance, and you have provided the correct database information in config.yml")
        quit()
        return

    # Get the current databases and check if the one we need is there
    dbs = await r.db_list().run(conn)
    if db_opts['db'] not in dbs:
        # If not, we want to create it
        print('Couldn\'t find database {}...creating now'.format(db_opts['db']))
        await r.db_create(db_opts['db']).run(conn)
        # Then add all the tables
        for table, key in required_tables.items():
            print("Creating table {}...".format(table))
            await r.table_create(table, primary_key=key).run(conn)
        print("Done!")
    else:
        # Otherwise, if the database is setup, make sure all the required tables are there
        tables = await r.table_list().run(conn)
        for table, key in required_tables.items():
            if table not in tables:
                print("Creating table {}...".format(table))
                await r.table_create(table, primary_key=key).run(conn)
    print("Done checking tables!")

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