from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from appconf import AppConf


class ServerStatusAppConf(AppConf):
    SERVICE_UNAVAILABLE = _("unavailable")
    SERVICE_AVAILABLE = _("ok")

    DISPLAY_EXCEPTIONS = True
    PLUGIN_MODULE_NAME = 'status_report'
    DEFAULT_GROUPNAME = _('Main')
