"""
Marshmallow Plugin Manager

Structure:
    PluginManager
        [MarshmallowModule]
            [MarshmallowCommand]
            [MarshmallowEvent]
"""

import os

from marshmallow.core.mechanics.command import MarshmallowCommand
from marshmallow.core.mechanics.module import MarshmallowModule
from marshmallow.core.mechanics.logger import create_logger

class PluginManager(object):
    def __init__(self, bot, init):
        self.log = create_logger('Plugin Manager')
        self.bot = bot
        self.prefix = bot.cfg.pref.prefix
        self.path = None
        self.init = init
        self.modules = {}
        self.load_all_modules()
        self._alts = {}

    @property
    def events(self):
        tmp = {}
        for module in self.modules.values():
            for name, evlist in module.events.items():
                tmp[name] = evlist

        return tmp

    @property
    def commands(self):
        tmp = {}
        for module in self.modules.values():
            for name, cmd in module.commands.items():
                tmp[name] = cmd

        return tmp

    @property
    def alts(self):
        tmp = {}
        for module in self.modules.values():
            tmp.update(module.alts)

        return tmp

    def load_module(self, file):
        mod_name, mod = MarshmallowModule.from_file(self, file)
        self.modules[mod_name] = mod
        return (mod_name, mod)

    def unload_module(self, name):
        pass

    def reload_module(self, name):
        pass

    def load_all_modules(self):
        self.plugin_files('sigma/modules', self.load_module)

    def plugin_files(self, directory, callback):
        for root, _dir, files in os.walk(directory):
            if 'module.yml' in files:
                callback(os.path.join(root, 'module.yml'))