from itertools import chain

from .base import BasePlugin
from .exceptions import NotRegistered, AlreadyRegistered


class ServerStatusPluginRegistry(object):

    def __init__(self):
        self._registry = {}

    def register(self, plugin, **options):
        plugin_instance = plugin()
        key = "{}:{}".format(plugin_instance.group, plugin_instance.name)

        if key in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % key)
        self._registry[key] = plugin_instance


    def unregister(self, plugin_or_iterable):
        """
        Unregisters the given plugin(s).

        If a plugin isn't already registered, this will raise NotRegistered.
        """
        if isinstance(plugin_or_iterable, BasePlugin):
            plugin_or_iterable = [plugin_or_iterable, ]

        for plugin in plugin_or_iterable:
            plugin_instance = plugin()
            key = "{}:{}".format(plugin_instance.group, plugin_instance.name)

            if key not in self._registry.values():
                raise NotRegistered('The plugin %s is not registered' % key)

            del self._registry[key]


plugins = ServerStatusPluginRegistry()
