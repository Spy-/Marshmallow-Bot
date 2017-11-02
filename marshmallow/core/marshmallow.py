import os
import errno
import arrow
import shutil
import discord
import pymongo

from marshmallow.core.mechanics.database import Database
from marshmallow.core.mechanics.config import Configuration
from marshmallow.core.mechanics.information import Information
from marshmallow.core.mechanics.logger import create_logger
from marshmallow.core.mechanics.plugman import PluginManager
from marshmallow.core.mechanics.cooldown import CooldownControl
from marshmallow.core.mechanics.music import MusicCore

init_cfg = Configuration()

# determines if this is an actual bot or a self bot hybrid
if init_cfg.dsc.bot:
    client_class = discord.AutoShardedClient
else:
    client_class = discord.Client


class Marshmallow(client_class):
    def __init__(self):
        super().__init__()
        self.ready = False
        # State attributes before initialization.
        self.log = None
        self.cfg = None
        self.db = None
        self.cool_down = None
        self.music = None
        self.modules = None
        #Initialize startup methods
        self.create_cache()
        self.init_logger()
        self.log.info('---------------------------------')
        self.init_config()
        self.log.info('---------------------------------')
        self.init_database()
        self.log.info('---------------------------------')
        self.init_cooldown()
        self.log.info('---------------------------------')
        self.init_music()
        self.log.info('---------------------------------')
        self.info = Information()
        self.init_modules(init=True)
        self.start_time = arrow.utcnow()
        self.message_count = 0
        self.command_count = 0

    #clears the cache folder
    @staticmethod
    def create_cache():
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.makedirs('cache')

    #creates the logger for the bot
    def init_logger(self):
        self.log = create_logger('Marshmallow')
        self.log.info('Logger Created')

    #loads info from the config files
    def init_config(self):
        self.log.info('Loading Configuration...')
        self.cfg = init_cfg
        self.log.info(f'Running as a Bot: {self.cfg.dsc.bot}')
        self.log.info(f'Default Bot Prefix: {self.cfg.pref.prefix}')
        self.log.info('Core Configuration Data Loaded')

    #connects to the mongo database
    def init_database(self):
        self.log.info('Connecting to Database...')
        self.db = Database(self, self.cfg.db)
        try:
            self.db.test.collection.find_one({})
        except pymongo.errors.ServerSelectionTimeoutError:
            self.log.error('A Connection To The Database Host Failed!')
            exit(errno.ETIMEDOUT)
        except pymongo.errors.OperationFailure:
            self.log.error('Database Access Operation Failed!')
            exit(errno.EACCES)
        self.log.info('Successfully Connected to Database')

    def init_cooldown(self):
        self.log.info('Loading Cooldown Controls...')
        self.cooldown = CooldownControl(self)
        self.log.info('Cooldown Controls Successfully Enabled')

    #loads up the music utility requirements for music to work
    def init_music(self):
        self.log.info('Loading Music Controller...')
        self.music = MusicCore(self)
        self.log.info('Music Controller Initialized and Ready')

    #tells the plugin manager to start loading modules
    def init_modules(self, init=False):
        if init:
            self.log.info('Loading Marshmallow Modules')
        self.modules = PluginManager(self, init)

    #helper function to find the bot prefix
    def get_prefix(self, message):
        prefix = self.cfg.pref.prefix
        if message.guild:
            pfx_search = self.db.get_guild_settings(message.guild.id, 'Prefix')
            if pfx_search:
                prefix = pfx_search
        return prefix

    #this function is called to actually start up the bot
    def run(self):
        try:
            self.log.info('Connecting to Discord Gateway...')
            super().run(self.cfg.dsc.token, bot=self.cfg.dsc.bot)
        except discord.LoginFailure:
            self.log.error('Invalid Token!')
            exit(errno.EPERM)

    #helper function that runs and creates events
    async def event_runner(self, event_name, *args):
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute(*args))

    #event for when the bot connects to a server/guild
    async def on_connect(self):
        event_name = 'connect'
        if event_name in self.modules.events:
            for event in self.modules.events[event_name]:
                self.loop.create_task(event.execute())

    #event for when the bot connects to a new shard
    async def on_shard_ready(self, shard_id):
        self.log.info(f'Connection to Discord Shard #{shard_id} Established')
        event_name = 'shard_ready'
        self.loop.create_task(self.event_runner(event_name, shard_id))

    #event for when the bot is done loading everything
    async def on_ready(self):
        self.ready = True
        self.log.info('---------------------------------')
        self.log.info('Marshmallow Fully Loaded and Ready')
        self.log.info('---------------------------------')
        self.log.info(f'User Account: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'User Snowflake: {self.user.id}')
        self.log.info('---------------------------------')
        self.log.info('Launching On-Ready Modules...')
        event_name = 'ready'
        self.loop.create_task(self.event_runner(event_name))
        self.log.info('All On-Ready Module Loops Created')
        self.log.info('---------------------------------')
        if os.getenv('CI_TOKEN'):
            self.log.info('Continuous Integration Environment Detected')
            exit()

    #event for when a message is sent in a discord server/guild
    async def on_message(self, message):
        self.message_count += 1
        if not message.author.bot:
            event_name = 'message'
            prefix = self.get_prefix(message)
            if message.content.startswith(prefix):
                args = message.content.split(' ')
                args = list(filter(lambda a: a != '', args))
                cmd = args.pop(0)[len(self.get_prefix(message)):].lower()
                if cmd in self.modules.alts:
                    cmd = self.modules.alts[cmd]
                if cmd in self.modules.commands:
                    self.loop.create_task(self.modules.commands[cmd].execute(message, args))
            self.loop.create_task(self.event_runner(event_name, message))
            if self.user.mentioned_in(message):
                event_name = 'mention'
                self.loop.create_task(self.event_runner(event_name, message))

    #event for when a user edits a message
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            event_name = 'message_edit'
            self.loop.create_task(self.event_runner(event_name, before, after))

    #event for when a user deletes a message
    async def on_message_delete(self, message):
        if not message.author.bot:
            event_name = 'message_delete'
            self.loop.create_task(self.event_runner(event_name, message))

    #event for when a user joins a server/guild that the bot is a member of
    async def on_member_join(self, member):
        if not member.bot:
            event_name = 'member_join'
            self.loop.create_task(self.event_runner(event_name, member))

    #event for when a user leaves a server/guild that the bot is a member of
    async def on_member_remove(self, member):
        if not member.bot:
            event_name = 'member_remove'
            self.loop.create_task(self.event_runner(event_name, member))

    #event for when a user changes something about themselves. ie: name, nickname, avatar
    async def on_member_update(self, before, after):
        if not before.bot:
            event_name = 'member_update'
            self.loop.create_task(self.event_runner(event_name, before, after))

    #event for when the bot joins a server/guild
    async def on_guild_join(self, guild):
        event_name = 'guild_join'
        self.loop.create_task(self.event_runner(event_name, guild))

    #event for when the bot leaves a server/guild
    async def on_guild_remove(self, guild):
        event_name = 'guild_remove'
        self.loop.create_task(self.event_runner(event_name, guild))

    #event for when a user or bot changes their voice state. ie: enters a voice channel, mutes, deafeans...
    async def on_voice_state_update(self, member, before, after):
        event_name = 'voice_state_update'
        self.loop.create_task(self.event_runner(event_name, member, before, after))