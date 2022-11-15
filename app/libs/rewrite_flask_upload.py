import os
import posixpath

from flask_uploads import UploadNotAllowed, UploadSet
from werkzeug.datastructures import FileStorage


class MyUploadNotAllowed(UploadNotAllowed):
    def extension(filename):
        ext = os.path.splitext(filename)[1]
        if ext == '':
            # add non-ascii filename support
            ext = os.path.splitext(filename)[0]
        if ext.startswith('.'):
            # os.path.splitext retains . separator
            ext = ext[1:]
        return ext


class MyUploadSet(UploadSet):
    def file_allowed(self, storage, basename):
        return self.extension_allowed(MyUploadNotAllowed.extension(basename))

    def save(self, storage, folder=None, name=None):
        if not isinstance(storage, FileStorage):
            raise TypeError("storage must be a werkzeug.FileStorage")

        if folder is None and name is not None and "/" in name:
            folder, name = os.path.split(name)

        basename = self.get_basename(storage.filename)

        if not self.file_allowed(storage, basename):
            raise MyUploadNotAllowed()

        if name:
            if name.endswith('.'):
                basename = name + MyUploadNotAllowed.extension(basename)
            else:
                basename = name

        if folder:
            target_folder = os.path.join(self.config.destination, folder)
        else:
            target_folder = self.config.destination
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        if os.path.exists(os.path.join(target_folder, basename)):
            basename = self.resolve_conflict(target_folder, basename)

        target = os.path.join(target_folder, basename)
        storage.save(target)
        if folder:
            return posixpath.join(folder, basename)
        else:
            return basename
