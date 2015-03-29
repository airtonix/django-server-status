from .conf import settings
from django.utils.translation import ugettext_lazy as _


class ServiceStatus(object):
    code = None
    message = None
    description = None

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


class ServiceOk(ServiceStatus):
    code = 'ok'
    message = _('Ok')


class ServiceException(ServiceStatus, Exception):
    pass


class ServiceUnavailable(ServiceException):
    code = 'unavailable'
    message = _('Unavailable')


class ServiceReturnedUnexpectedResult(ServiceException):
    code = 'unexpected'
    message = _('Unexpected Results')


class ServiceUnstable(ServiceException):
    code = 'unstable'
    message = _('Unstable')


class ServiceFatal(ServiceException):
    code = 'fatal'
    message = _('Fatal Errors')


class AlreadyRegistered(Exception):
    code = 'already-registered'


class NotRegistered(Exception):
    code = 'not-registered'


BadStatusCases = (
    ServiceFatal,
    ServiceUnavailable,
    ServiceUnstable,
)

GoodStatusCases = (
    ServiceOk,
    )
