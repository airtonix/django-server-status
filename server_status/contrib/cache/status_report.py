from django.core.cache.backends.base import CacheKeyWarning
from django.core.cache import cache

from server_status.backends.base import BaseServerStatusPlugin
from server_status.exceptions import ServiceUnavailable, ServiceReturnedUnexpectedResult
from server_status.registry import plugins


@plugins.register
class CacheBackend(BaseServerStatusPlugin):

    def check_status(self):
        try:
            cache.set('serverstatus_test', 'somethingsomethingsomething', 1)
            if cache.get("serverstatus_test") == "somethingsomethingsomething":
                return True

            else:
                raise ServiceUnavailable("Cache key does not match")

        except CacheKeyWarning:
            raise ServiceReturnedUnexpectedResult("Cache key warning")

        except ValueError:
            raise ServiceReturnedUnexpectedResult("ValueError")

        except Exception:
            raise ServiceUnavailable("Unknown exception")
