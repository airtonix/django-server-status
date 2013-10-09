from django.db.models.options import get_verbose_name

from .registry import plugins
from .base import BaseServerStatusPlugin


def server_status(func_or_name, group=None):
    """
    Usage:

        @server_status("My Check")
        def my_check():
            if something_is_not_okay():
                raise ServiceReturnedUnexpectedResult()

        @server_status
        def other_check():
            if something_is_not_available():
                raise ServiceUnavailable()
    """
    def inner(func):
        Plugin = type(func.__name__, (BaseServerStatusPlugin,), {'_wrapped': staticmethod(func)})
        Plugin.identifier = name
        plugins.register(Plugin, group=group)
        return func

    if callable(func_or_name):
        name = get_verbose_name(func_or_name.__name__).replace('_', ' ')
        return inner(func_or_name)

    else:
        name = func_or_name
        return inner
