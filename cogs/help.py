import asyncio
import collections
import datetime
import inspect
import itertools
import re
import sys
import time
import traceback
from enum import Enum
from random import choice, randint
from urllib.parse import quote_plus

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import formatter

empty = u'\u200b'


_mentions_transforms = {
    '@everyone': '@\u200beveryone',
    '@here': '@\u200bhere'
}


def rewrite():
    return discord.version_info.major == 1


_mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))


orig_help = None


class Help(formatter.HelpFormatter):
    """Formats help for commands."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        global orig_help
        orig_help = bot.get_command('help')
        self.bot.remove_command('help')
        self.bot.formatter = self
        self.bot.help_formatter = self
        super().__init__(*args, **kwargs)

    # Shortcuts that allow cog to run on 0.16.8 and 1.0.0a

    def pm_check(self, ctx):
        if rewrite():
            return isinstance(ctx.channel, discord.DMChannel)
        else:
            return ctx.message.channel.is_private

    @property
    def me(self):
        if rewrite():
            return self.context.me
        else:
            return self.context.message.server.me

    @property
    def bot_all_commands(self):
        if rewrite():
            return self.bot.all_commands
        else:
            return self.bot.commands

    @property
    def avatar(self):
        if rewrite():
            return self.bot.user.avatar_url_as(format='png')
        else:
            return self.bot.user.avatar_url  # TODO: I really don't like not having a PNG

    @property
    def color(self):
        if self.pm_check(self.context):
            return 0
        else:
            return self.me.color

    async def send(self, dest, content=None, embed=None):
        if rewrite():
            await dest.send(content=content, embed=embed)
        else:
            await self.bot.send_message(dest, content=content, embed=embed)

    # All the other shit

    @property
    def author(self):
        # Get author dict with username if PM and display name in guild
        if self.pm_check(self.context):
            name = self.bot.user.name
        else:
            name = self.me.display_name if not '' else self.bot.user.name
        author = {
                'name': '{0} Help Manual'.format(name),
                'icon_url': self.avatar
            }
        return author

    @property
    def destination(self):
        return self.context.message.author if self.bot.pm_help else self.context.message.channel

    def _add_subcommands(self, cmds):
        entries = ''
        for name, command in cmds:
            if name in command.aliases:
                # skip aliases
                continue

            if self.is_cog() or self.is_bot():
                name = '{0}'.format(name)
                #name = '{0}{1}'.format(self.clean_prefix, name)

            entries += '`{0}` '.format(name)#, command.short_doc)
        return entries

    def get_ending_note(self):
        # command_name = self.context.invoked_with
        return "Type {0}help <command> for more info on a command.\n" \
               "You can also type {0}help <category> for more info on a category.".format(self.clean_prefix)

    async def format(self, ctx, command):
        """Formats command for output.
        Returns a dict used to build embed"""

        # All default values for embed dict
        self.command = command
        self.context = ctx
        emb = {
            'embed': {
                'title': '',
                'description': '',
            },
            'footer': {
                'text': self.get_ending_note()
            },
            'fields': []
        }

        description = command.description if not self.is_cog() else inspect.getdoc(command)
        if not description == '' and description is not None:
            description = '*{0}*'.format(description)

        if description:
            # <description> portion
            emb['embed']['description'] = description

        if isinstance(command, discord.ext.commands.core.Command):
            # <signature portion>
            emb['embed']['title'] = emb['embed']['description']
            #emb['embed']['description'] = '`Syntax: {0}`'.format(self.get_command_signature())

            # <long doc> section
            if command.help:
                name = '__{0}__'.format(command.help.split('\n')[0])
                name_length = len(name) - 4
                value = command.help[name_length:].replace('[p]', self.clean_prefix)
                if value == '':
                    value = empty
                field = {
                    'name': name,
                    'value': value,
                    'inline': False
                }
                emb['fields'].append(field)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                return emb

        def category(tup):
            # Turn get cog (Category) name from cog/list tuples
            cog = tup[1].cog_name
            return '**__{0}:__**'.format(cog) if cog is not None else '**__\u200bNo Category:__**'

        # Get subcommands for bot or category
        if rewrite():
            filtered = await self.filter_command_list()
        else:
            filtered = self.filter_command_list()

        if self.is_bot():
            # Get list of non-hidden commands for bot.
            data = sorted(filtered, key=category)
            for category, commands in itertools.groupby(data, key=category):
                # there simply is no prettier way of doing this.
                field = {
                    'inline': False
                }
                commands = sorted(commands)
                if len(commands) > 0:
                    field['name'] = category
                    field['value'] = self._add_subcommands(commands)  # May need paginated
                    emb['fields'].append(field)

        else:
            # Get list of commands for category
            filtered = sorted(filtered)
            if filtered:
                field = {
                    'name': '**__Commands:__**' if not self.is_bot() and self.is_cog() else '**__Subcommands:__**',
                    'value': self._add_subcommands(filtered),  # May need paginated
                    'inline': False
                }

                emb['fields'].append(field)

        return emb

    async def format_help_for(self, ctx, command_or_bot, reason: str=None):
        """Formats the help page and handles the actual heavy lifting of how  ### WTF HAPPENED?
        the help command looks like. To change the behaviour, override the
        :meth:`~.HelpFormatter.format` method.
        Parameters
        -----------
        ctx: :class:`.Context`
            The context of the invoked help command.
        command_or_bot: :class:`.Command` or :class:`.Bot`
            The bot or command that we are getting the help of.
        Returns
        --------
        list
            A paginated output of the help command.
        """
        self.context = ctx
        self.command = command_or_bot
        emb = await self.format(ctx, command_or_bot)

        if reason:
            emb['embed']['title'] = "{0}".format(reason)

        embed = discord.Embed(color=self.color, **emb['embed'])
        embed.set_author(**self.author)
        for field in emb['fields']:
            embed.add_field(**field)
        embed.set_footer(**emb['footer'])
        await self.send(self.destination, embed=embed)

    def simple_embed(self, title=None, description=None, color=None, author=None):
        # Shortcut
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=self.bot.formatter.get_ending_note())
        if author:
            embed.set_author(**author)
        return embed

    def cmd_not_found(self, cmd, color=0):
        # Shortcut for a shortcut. Sue me
        embed = self.simple_embed(title=self.bot.command_not_found.format(cmd),
                                  description='Commands are case sensitive. Please check your spelling and try again',
                                  color=color, author=self.author)
        return embed

    @commands.command(name='help', pass_context=True)
    async def help(self, ctx, *cmds: str):
        """Shows help documentation.
        [p]**help**: Shows the help manual.
        [p]**help** command: Show help for a command
        [p]**help** Category: Show commands and description for a category"""
        self.context = ctx

        def repl(obj):
            return _mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(cmds) == 0:
            #await self.bot.formatter.format_help_for(ctx, self.bot)
            #return
            """Embedded help command"""
            author = ctx.message.author
            self.context = ctx
            msg = "**Command list:**"
            color = self.color  # 0xffa500
            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if self.bot.commands[com].module.__name__ not in com_groups:
                        com_groups.append(self.bot.commands[com].module.__name__)
                    else:
                        continue
                except Exception as e:
                    print(e)
                    continue
            com_groups.sort()
            alias = []
            # print(com_groups)
            for com_group in com_groups:
                commands = []
                for com in self.bot.commands:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if com in self.bot.commands[com].aliases:
                        continue
                    if com_group == self.bot.commands[com].module.__name__:
                        commands.append(com)
                final_coms[com_group] = commands
            to_send = []
            final_coms = collections.OrderedDict(sorted(final_coms.items()))
            field_count = 0
            page = 0
            counter = 0
            for group in final_coms:
                counter += 1
                if field_count == 0:
                    page += 1
                    title = "**Command list,** page {}".format(page)
                    em = discord.Embed(description=title, color=color)
                field_count += 1
                is_last = counter == len(final_coms)
                msg = ""
                final_coms[group].sort()
                count = 0
                for com in final_coms[group]:
                    if count == 0:
                        msg += '`{}`'.format(com)
                    else:
                        msg += ', `{}`'.format(com)
                    count += 1
                cog_name = group.replace("cogs.", "").title()
                cog = "```\n"
                cog += cog_name
                cog += "\n```"
                em.add_field(name=cog, value=msg, inline=False)
                if field_count == 15 or is_last:
                    to_send.append(em)
                    field_count = 0
            for em in to_send:
                await self.bot.say(embed=em)

        elif len(cmds) == 1:
            # try to see if it is a cog name
            name = _mention_pattern.sub(repl, cmds[0])
            command = None
            if name in self.bot.cogs:
                command = self.bot.cogs[name]
            else:
                command = self.bot_all_commands.get(name)
                if command is None:
                    await self.send(self.destination, embed=self.cmd_not_found(name, self.color))
                    return

            await self.bot.formatter.format_help_for(ctx, command)
        else:
            name = _mention_pattern.sub(repl, cmds[0])
            command = self.bot_all_commands.get(name)
            if command is None:
                await self.send(self.destination, embed=self.cmd_not_found(name, self.color))
                return

            for key in cmds[1:]:
                try:
                    key = _mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await self.send(self.destination, embed=self.cmd_not_found(key, self.color))
                        return
                except AttributeError:
                    await self.send(self.destination,
                                    embed=self.simple_embed(title=
                                                            'Command "{0.name}" has no subcommands.'.format(command),
                                                            color=self.color,
                                                            author=self.author))
                    return

            await self.bot.formatter.format_help_for(ctx, command)

    @help.error
    async def help_error(self, error, ctx):
        await self.send(self.destination, '{0.__name__}: {1}'.format(type(error), error))
        traceback.print_tb(error.original.__traceback__, file=sys.stderr)

    def __unload(self):
        print('called __unload')
        self.bot.formatter = formatter.HelpFormatter()
        self.bot.add_command(orig_help)

def setup(bot):
    bot.add_cog(Help(bot))
