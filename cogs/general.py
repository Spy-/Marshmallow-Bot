import asyncio
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

from utilities.chat_formatting import *


def rewrite():
    return discord.version_info.major == 1


class General:
    """General Utility Commands"""
    #choose, ping, help, ping, info, uptime

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args, **kwargs)

    @property
    def me(self):
        if rewrite():
            return self.context.me
        else:
            return self.context.message.server.me

    @property
    def color(self):
        if self.pm_check(self.context):
            return 0
        else:
            return self.me.color

    def pm_check(self, ctx):
        if rewrite():
            return isinstance(ctx.channel, discord.DMChannel)
        else:
            return ctx.message.channel.is_private

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Returns the ping of the bot"""
        self.context = ctx
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await self.bot.send_typing(channel)
        t2 = time.perf_counter()
        msg = "Ping **{}ms**".format(round((t2-t1)*1000))
        embed = discord.Embed(title="Pong!", description=msg, color=self.me.color)
        await self.bot.say(embed=embed)

    @commands.command()
    async def choose(self, *choices):
        """Chooses between multiple choices.
        To denote multiple choices, you should use double quotes.
        """
        choices = [escape_mass_mentions(c) for c in choices]
        if len(choices) < 2:
            embed = discord.Embed(title="Choose - Error", description="Not enough choices to pick from.", color=self.me.color)
            await self.bot.say("Not enough choices to pick from")
        else:
            embed = discord.Embed(title="Choose", description=choice(choices), color=self.me.color)
            await self.bot.say(choice(choices))

    @commands.command(pass_context=True)
    async def roll(self, ctx, number: int = 100):
        """Rolls random number (between 1 and user choice)
        Defaults to 100.
        """
        self.context = ctx
        author = ctx.message.author
        if number > 1:
            n = randint(1, number)
            description="{} :game_die: {} :game_die:".format(author.mention, n)
            embed = discord.Embed(title="Roll", description=description, color=self.me.color)
            await self.bot.say(description)
        else:
            embed = discord.Embed(title="Roll - Error", description="{} Maybe higher than 1? ;P".format(author.mention), color=self.me.color)
            await self.bot.say(embed = embed)

    @commands.command(pass_context=True)
    async def test(self):
        await self.bot.say(warning("hello"))

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def userinfo(self, ctx, *, user: discord.Member=None):
        """Shows users's informations"""
        self.context = ctx
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = self.fetch_joined_at(user, server)
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="Member #{} | User ID:{}"
                             "".format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server's informations"""
        self.context = ctx
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        #colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        #colour = int(colour, 16)
        colour = self.me.color

        data = discord.Embed(
            description=created_at,
            colour=colour) #discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at
    
def setup(bot):
    bot.add_cog(General(bot))
