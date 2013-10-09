from django.utils.translation import ugettext_lazy as _

from .conf import settings
from . import exceptions


class BasePlugin(object):
    _name = None
    _group = None

    def __init__(self,*args,**kwargs):
        super(BasePlugin, self).__init__(*args, **kwargs)

    def check_status(self):
        return NotImplementedError(_("You need to override `BasePlugin.check_status` in your StatusPlugin"))

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group(self):
        return self._group if self._group else settings.SERVER_STATUS_DEFAULT_GROUPNAME
    @group.setter
    def group(self, value):
        self._group = value

    @property
    def status(self):
        if not getattr(self, "_status", False):
            try:
                result = self.check_status()

                if isinstance(result, exceptions.ServiceException):
                    raise result

                if isinstance(result, bool) and result is False:
                    raise exceptions.ServiceUnstable

                setattr(self, '_status', exceptions.ServiceOk)

            except exceptions.BadStatusCases as error:
                setattr(self, "_status", error)

            except Exception as error:
                print error

        return self._status

    @classmethod
    def identifier(cls):
        return cls.__name__


class BaseServerStatusPlugin(BasePlugin):

    def check_status(self):
        self._wrapped()
