import os
import sys
import codecs
import shutil
import logging
import configparser

from cogs.utils.exceptions import HelpfulError

log = logging.getLogger(__name__)

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.find_config()

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        confsections = {"Credentials", "Permissions", "Chat", "Music", "Misc", "Keys"}.difference(config.sections())
        if confsections:
            msg = ("One or more required config sections are missing. Fix your config. Each [Section] should be on its own line with ",
                  "nothing else on it. The following sections are missing: {}".format(', '.join(['[%s]' % s for s in confsections])))
            preface = "An error has occured parsing the config:\n"
            raise HelpfulError(msg, preface)

        self._confpreface = "An error has occured reading the config:\n"
        self._confpreface2 = "An error has occured validating the config:\n"

        self.token = config.get('Credentials', 'Token', fallback=None)
        self.email = config.get('Credentials', 'Email', fallback=None)
        self.password = config.get('Credentials', 'Password', fallback=None)
        self.auth = None

        self.owner_id = config.get('Permissions', 'OwnerID', fallback=ConfigDefaults.owner_id)
        self.OAuth = config.get('Permissions', 'Auth', fallback=None)

        self.command_prefix = config.get('Chat', 'CommandPrefix', fallback=ConfigDefaults.command_prefix)
        self.delete_messages = config.getboolean('Chat', 'DeleteMessages', fallback=ConfigDefaults.delete_messages)
        self.delete_invoking = config.getboolean('Chat', 'DeleteInvoking', fallback=ConfigDefaults.delete_invoking)

        self.default_volume = config.getfloat('Music', 'DefaultVolume', fallback=ConfigDefaults.default_volume)
        self.skips_required = config.getint('Music', 'SkipsRequired', fallback=ConfigDefaults.skips_required)
        self.skips_ratio = config.getfloat('Music', 'SkipRatio', fallback=ConfigDefaults.skip_ratio_required)
        self.save_videos = config.getboolean('Music', 'SaveVideos', fallback=ConfigDefaults.save_videos)
        self.now_playling_mentions = config.getboolean('Music', 'NowPlayingMentions', fallback=ConfigDefaults.now_playing_mentions)
        self.use_auto_playlist = config.getboolean('Music', 'UseAutoPlaylist', fallback=ConfigDefaults.auto_playlist)
        self.auto_pause = config.getboolean('Music', 'AutoPause', fallback=ConfigDefaults.auto_pause)
        self.persistent_queue = config.getboolean('Music', 'PersistentQueue', fallback=ConfigDefaults.persistent_queue)

        self.debug_level = config.get('Music', 'DebugLevel', fallback=ConfigDefaults.debug_level)
        self.debug_level_str = self.debug_level
        self.debug_mode = False

        self.description = config.get('Misc', 'Description', fallback="description")
        self.default_status = config.get('Misc', 'DefaultStatus', fallback=None)

        self.discord_bots_key = config.get('Keys', 'DiscordBotsKey', fallback=None)
        self.carbon_key = config.get('Keys', 'CarbonKey', fallback=None)
        self.twitch_key = config.get('Keys', 'TwitchKey', fallback=None)
        self.youtube_key = config.get('Keys', 'YoutubeKey', fallback=None)
        self.osu_key = config.get('Keys', 'OsuKey', fallback=None)

        self.run_checks()

    def run_checks(self):
        """
        Validates Config Logic
        """

        if self.email or self.password:
            msg = "Use a token instead. Email and password will be supported soon"
            raise HelpfulError(msg, self._confpreface)
        
        elif not self.token:
            msg = "No login credentials were specified in the config. Please fill in the token field"
            raise HelpfulError(msg, self._confpreface)
        
        else:
            self.auth = self.token

        if self.owner_id:
            self.owner_id = self.owner_id.lower()

            if self.owner_id.isdigit():
                if int(self.owner_id) < 10000:
                    raise HelpfulError(
                        "An invalid OwnerID was set: {}".format(self.owner_id),

                        "Correct your OwnerID.  The ID should be just a number, approximately "
                        "18 characters long.  If you don't know what your ID is, read the "
                        "instructions in the options or ask in the help server.",
                        preface=self._confpreface
                    )

            elif self.owner_id == 'auto':
                pass # defer to async check

            else:
                self.owner_id = None

        if not self.owner_id:
            msg = "No OwnerID was set. Please set the OwnerID option in {}".format(self.config_file)
            raise HelpfulError(msg, preface=self._confpreface)

        if self.bound_channels:
            try:
                self.bound_channels = set(x for x in self.bound_channels.split() if x)
            except:
                log.warning("BindToChannels data is invalid, will not bind to any channels")
                self.bound_channels = set()

        if self.autojoin_channels:
            try:
                self.autojoin_channels = set(x for x in self.autojoin_channels.split() if x)
            except:
                log.warning("AutojoinChannels data is invalid, will not autojoin any channels")
                self.autojoin_channels = set()

        self.delete_invoking = self.delete_invoking and self.delete_messages

        self.bound_channels = set(item.replace(',', ' ').strip() for item in self.bound_channels)

        self.autojoin_channels = set(item.replace(',', ' ').strip() for item in self.autojoin_channels)

        ap_path, ap_name = os.path.split(self.auto_playlist_file)
        apn_name, apn_ext = os.path.splitext(ap_name)
        self.auto_playlist_removed_file = os.path.join(ap_path, apn_name + '_removed' + apn_ext)

        if hasattr(logging, self.debug_level.upper()):
            self.debug_level = getattr(logging, self.debug_level.upper())
        else:
            log.warning("Invalid DebugLevel option \"{}\" given, falling back to INFO".format(self.debug_level_str))
            self.debug_level = logging.INFO
            self.debug_level_str = 'INFO'

        self.debug_mode = self.debug_level <= logging.DEBUG

    async def async_validate(self, bot):
        log.debug("Validating options...")

        if self.owner_id == 'auto':
            if not bot.user.bot:
                msg = "Invalid parameter \"auto\" for OwnerID option. Only bot accounts can use the \"auto\" option.  Please set the OwnerID in the config."
                raise HelpfulError(msg,  preface=self._confpreface2)

            self.owner_id = bot.cached_app_info.owner.id
            log.debug("Aquired owner id via API")

        if self.owner_id == bot.user.id:
            msg = "Your OwnerID is incorrect or you've used the wrong credentials.",
                  "The bot's user ID and the id for OwnerID is identical.  ",
                  "This is wrong.  The bot needs its own account to function, ",
                  "meaning you cannot use your own account to run the bot on.  ",
                  "The OwnerID is the id of the owner, not the bot.  ",
                  "Figure out which one is which and use the correct information."
            raise HelpfulError(msg, preface=self._confpreface2)


    def find_config(self):
        config = configparser.ConfigParser(interpolation=None)

        if not os.path.isfile(self.config_file):
            if os.path.isfile(self.config_file + '.ini'):
                shutil.move(self.config_file + '.ini', self.config_file)
                log.info("Moving {0} to {1}, you should probably turn file extensions on.".format(
                    self.config_file + '.ini', self.config_file
                ))

            elif os.path.isfile('config/example_options.ini'):
                shutil.copy('config/example_options.ini', self.config_file)
                log.warning('Options file not found, copying example_options.ini')

            else:
                raise HelpfulError("Your config files are missing.  Neither options.ini nor example_options.ini were found.",
                                   "Grab the files back from the archive or remake them yourself and copy paste the content "
                                   "from the repo.  Stop removing important files!")

        if not config.read(self.config_file, encoding='utf-8'):
            c = configparser.ConfigParser()
            try:
                # load the config again and check to see if the user edited that one
                c.read(self.config_file, encoding='utf-8')

                if not int(c.get('Permissions', 'OwnerID', fallback=0)): # jake pls no flame
                    print(flush=True)
                    log.critical("Please configure config/options.ini and re-run the bot.")
                    sys.exit(1)

            except ValueError: # Config id value was changed but its not valid
                raise HelpfulError(
                    'Invalid value "{}" for OwnerID, config cannot be loaded.'.format(
                        c.get('Permissions', 'OwnerID', fallback=None)
                    ),
                    "The OwnerID option takes a user id, fuck it i'll finish this message later."
                )

            except Exception as e:
                print(flush=True)
                log.critical("Unable to copy config/example_options.ini to {}".format(self.config_file), exc_info=e)
                sys.exit(2)

    def find_autoplaylist(self):
        if not os.path.exists(self.auto_playlist_file):
            if os.path.exists('config/_autoplaylist.txt'):
                shutil.copy('config/_autoplaylist.txt', self.auto_playlist_file)
                log.debug("Copying _autoplaylist.txt to autoplaylist.txt")
            else:
                log.warning("No autoplaylist file found.")


    def write_default_config(self, location):
        pass

class ConfigDefaults:
    owner_id = None
    dev_ids = set()

    command_prefix = '?'
    bound_channels = set()
    autojoin_channels = set()

    default_volume = 0.15
    skips_required = 4
    skip_ratio_required = 0.5
    save_videos = True
    now_playing_mentions = False
    auto_summon = True
    auto_playlist = True
    auto_pause = True
    delete_messages = True
    delete_invoking = False
    persistent_queue = True
    debug_level = 'INFO'

    options_file = 'config/options.ini'
    blacklist_file = 'config/blacklist.txt'
    auto_playlist_file = 'config/autoplaylist.txt'

setattr(ConfigDefaults, codecs.decode(b'ZW1haWw=', '\x62\x61\x73\x65\x36\x34').decode('ascii'), None)
setattr(ConfigDefaults, codecs.decode(b'cGFzc3dvcmQ=', '\x62\x61\x73\x65\x36\x34').decode('ascii'), None)
setattr(ConfigDefaults, codecs.decode(b'dG9rZW4=', '\x62\x61\x73\x65\x36\x34').decode('ascii'), None)

# These two are going to be wrappers for the id lists, with add/remove/load/save functions
# and id/object conversion so types aren't an issue
class Blacklist:
    pass

class Whitelist:
    pass