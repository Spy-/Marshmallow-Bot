import discord
from itertools import zip_longest
from marshmallow.core.utilities.constants import *


class GlobalCommandPermissions(object):
    def __init__(self, command, message):
        self.user = message.author
        self.server = message.guild
        self.message = message
        self.bot = command.bot
        self.cmd = command
        self.db = command.db

        self.short_perm = ['u', 's', 'm', 'o', 'd', 'n', 'v']
        perms = ["black_user", "black_srv", "module_denied",
                 "owner_denied", "dm_denied", "nsfw_denied", "partner_denied", ]
        self.permissions = dict(zip_longest(perms, [False], fillvalue=False))

        self.check_nsfw()
        self.check_dmable()
        self.check_black_srv()
        self.check_black_usr()
        self.check_owner()

    def check_dmable(self):
        if not self.message.guild:
            self.permissions['dm_denied'] = not self.cmd.dmable
        return self.permissions['dm_denied']

    def check_nsfw(self):
        if isinstance(self.message.channel, discord.TextChannel):
            if self.cmd.nsfw:
                self.permissions['nsfw_denied'] = not self.message.channel.is_nsfw(
                )
        return self.permissions['nsfw_denied']

    def check_black_mdl(self, file):
        self.permissions['module_denied'] = self.cmd.category in file.get(
            'Modules', {})
        return self.permissions['module_denied']

    def check_black_usr(self):
        black_user_collection = self.db[self.bot.cfg.db.database].BlacklistedUsers
        black_user_file = black_user_collection.find_one(
            {'UserID': self.message.author.id})
        if black_user_file:
            if 'Total' in black_user_file:
                if black_user_file['Total']:
                    self.permissions['black_user'] = True
                else:
                    self.permissions['black_user'] = self.check_black_mdl(
                        black_user_file)
            else:
                self.permissions['black_user'] = self.check_black_mdl(
                    black_user_file)

    def check_black_srv(self):
        if self.message.guild:
            black_srv_collection = self.db[self.bot.cfg.db.database].BlacklistedServers
            black_srv_file = black_srv_collection.find_one(
                {'ServerID': self.message.guild.id})
            if black_srv_file:
                self.permissions['black_srv'] = True

    def check_owner(self):
        auth = self.message.author
        ownrs = self.bot.cfg.dsc.owners
        if self.cmd.owner and auth.id not in ownrs:
            self.permissions['owner_denied'] = True

    @property
    def permitted(self):
        return not any(self.permissions.values())

    @property
    def permission_string(self):
        """
        Uppercase letters mean no permission, lowercase ones mean permission granted.

        U: User Blacklist
        S: Server Blacklist
        M: Module Blacklist
        O: Bot Owner
        D: Direct Message
        N: NSFW Usage
        V: Partner
        """

        tmp = ''
        for i, denied in enumerate(self.permissions.values()):
            tmp += (self.short_perm[i].upper()
                    if denied else self.short_perm[i])
        return tmp

    @property
    def response(self):
        if self.permissions['black_srv']:
            return
        elif self.permissions['black_user']:
            return
        elif self.permissions['dm_denied']:
            color = 0xBE1931
            title = f'⛔ Can\'t Be Used In Direct Messages'
            desc = f'Please use {self.bot.get_prefix(self.message)}{self.cmd.name} on a server where I am present.'
        elif self.permissions['owner_denied']:
            color = 0xBE1931
            title = '⛔ Bot Owner Only'
            desc = f'I\'m sorry {self.message.author.display_name}. I\'m afraid I can\'t let you do that.'
            desc += f'\nUnless you are in the `{self.bot.get_prefix(self.message)}owners` list, you can not use that.'
        elif self.permissions['nsfw_denied']:
            if self.message.guild:
                color = 0x744EAA
                title = f'🍆 NSFW Commands Are Not Allowed In #{self.message.channel.name}'
                desc = 'Make sure the NSFW marker is enabled in the channel settings.'
            else:
                return
        elif self.permissions['partner_denied']:
            color = 0x3B88C3
            title = '💎 Partner Servers Only'
            desc = 'Some commands are limited to only be usable by partners.'
            desc += '\nYou can request to be a partner server by visiting our '
            desc += 'server and telling us why you should be one.'
            desc += '\nYou can also become a partner by supporting us via our '
            desc += '[`Patreon`](https://www.patreon.com/ApexSigma) page.'
        else:
            return

        response = discord.Embed(color=color)
        response.add_field(name=title, value=desc)
        return response


class ServerCommandPermissions(object):
    def __init__(self, command, message):
        self.cmd = command
        self.db = self.cmd.db
        self.bot = self.cmd.bot
        self.msg = message
        self.permitted = self.check_perms()

    def check_overwrites(self, perms):
        overwritten = False
        cmd_exc = perms['CommandExceptions']
        mdl_exc = perms['ModuleExceptions']
        author = self.msg.author
        if cmd_exc:
            if self.cmd.name in cmd_exc:
                exceptions = cmd_exc[self.cmd.name]
                if author.id in exceptions['Users']:
                    overwritten = True
                if self.msg.channel.id in exceptions['Channels']:
                    overwritten = True
                for role in author.roles:
                    if role.id in exceptions['Roles']:
                        overwritten = True
                        break
        if mdl_exc:
            mdl_name = self.cmd.plugin_info['category']
            if mdl_name in mdl_exc:
                exceptions = mdl_exc[mdl_name]
                if author.id in exceptions['Users']:
                    overwritten = True
                if self.msg.channel.id in exceptions['Channels']:
                    overwritten = True
                for role in author.roles:
                    if role.id in exceptions['Roles']:
                        overwritten = True
                        break
        return overwritten

    def check_perms(self):
        if self.msg.guild:
            author = self.msg.author
            is_guild_admin = author.permissions_in(
                self.msg.channel).administrator
            if not is_guild_admin and author.id not in self.bot.cfg.dsc.owners:
                # Crunderwood was here...
                perms = self.db[self.bot.cfg.db.database].Permissions.find_one(
                    {'ServerID': self.msg.guild.id})
                if not perms:
                    permitted = True
                else:
                    cmd = self.cmd.name
                    mdl = self.cmd.plugin_info['category']
                    if mdl in perms['DisabledModules'] or cmd in perms['DisabledCommands']:
                        if self.check_overwrites(perms):
                            permitted = True
                        else:
                            permitted = False
                    else:
                        permitted = True
            else:
                permitted = True
        else:
            permitted = True
        return permitted
