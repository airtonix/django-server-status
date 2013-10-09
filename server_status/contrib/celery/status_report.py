from time import sleep
from datetime import datetime, timedelta

from server_status.base import BaseServerStatusPlugin
from server_status.registry import plugins
from server_status import exceptions

from .tasks import add


@plugins.register
class CeleryBasicTest(BaseServerStatusPlugin):
    _name = "Basic operations"
    _group = "Message Queue"

    def check_status(self):
        try:
            result = add.apply_async(args=[4, 4], expires=datetime.now() + timedelta(seconds=3), connect_timeout=3)
            now = datetime.now()

            while (now + timedelta(seconds=3)) > datetime.now():
                if result.result == 8:
                    return True
                sleep(0.5)

        except IOError:
            pass

        except Exception as error:
            raise exceptions.ServiceUnavailable(description=error)

