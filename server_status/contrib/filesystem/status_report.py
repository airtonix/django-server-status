from time import sleep
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.contrib.webdesign import lorem_ipsum

from server_status.conf import settings
from server_status.base import BaseServerStatusPlugin
from server_status.registry import plugins
from server_status import exceptions


class BaseFileSystemTest(BaseServerStatusPlugin):
    _name = "Filesystems"
    _group = "Storage"

    storage = None
    filename_pattern = 'health_check_storage_test/test-{}-{}.txt'

    def get_storage(self):
        if isinstance(self.storage, basestring):
            return get_storage_class(self.storage)()
        else:
            return self.storage

    def get_file_name(self):
        return self.filename_pattern.format(datetime.datetime.now(),
                                            random.randint(10000, 99999))

    def get_file_content(self):
        # select 64 random lorem lipsum words.
        return lorem_lipsum.words(64)

    def check_status(self):
        try:
            # write the file to the storage backend
            storage = self.get_storage()
            file_name = self.get_file_name()
            file_content = self.get_file_content()

            # save the file
            file_name = storage.save(
                file_name, ContentFile(content=file_content))
            # read the file and compare
            f = storage.open(file_name)
            if not storage.exists(file_name):
                raise exceptions.ServiceUnavailable(
                    code="error",
                    description=_("Filesystem is currently in a readonly state."))

            if not f.read() == file_content:
                raise exceptions.ServiceUnavailable(
                    code="error",
                    message=_("Filesystem is content doesn't match"))

            # delete the file and make sure it is gone
            storage.delete(file_name)
            if storage.exists(file_name):
                raise exceptions.ServiceUnavailable(
                    code="error",
                    message=_("File was not deleted"))

            return True

        except Exception:
            raise exceptions.ServiceUnstable(
                    code="error",
                    message="unknown problems")


@plugins.register
class DefaultFileStorageHealthCheck(BaseFileSystemTest):
    storage = settings.DEFAULT_FILE_STORAGE
