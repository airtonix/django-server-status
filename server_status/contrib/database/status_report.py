from django.db import DatabaseError, IntegrityError
from django.utils.translation import ugettext_lazy as _

from server_status.base import BaseServerStatusPlugin
from server_status.registry import plugins
from server_status import exceptions

from . import models


@plugins.register
class DjangoDatabaseBackend(BaseServerStatusPlugin):
    name = _("ORM")
    group = _("Database")
    def check_status(self):
        try:
            obj = models.TestModel.objects.create(title="test")
            obj.title = "newtest"
            obj.save()
            obj.delete()
            return True

        except IntegrityError:
            raise exceptions.ServiceUnstable(message=_("Integrity Error"))

        except DatabaseError:
            raise exceptions.ServiceFatal(message=_("Database error"))

