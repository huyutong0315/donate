import datetime
import os
import shutil

from app.api import photo, audio


class File:
    file_type = None
    sets = None

    def __init__(self, sets=None):
        self.sets = sets
        self.file_type = sets.__dict__.get('name')

    def get_file_url(self, fname):
        if fname is not None and fname != '':
            return self.sets.url(fname)

    @staticmethod
    def delete_file(path):
        if path is not None and path != '':
            if os.path.exists(path):
                os.remove(path)

    @staticmethod
    def delete_folder(path):
        if path is not None and path != '':
            if os.path.exists(path):
                shutil.rmtree(path)

    def get_file_path(self, fname):
        if fname is not None and fname != '':
            return self.sets.path(fname)

    def upload_file(self, file):
        # 这里一个bug， postman传过来的中文文件最后加了个"
        # if file.filename.endswith('\"'):
        #     file.filename = file.filename[:-1]

        #     (folder, extension) = os.path.splitext(file.filename)
        #     extension = extension[1:]
        #     if extension in ('png', 'jpg'):
        #         self.sets = photo
        #         self.file_type = 'photo'
        #     elif extension in ('wav', 'mp3'):
        #         self.sets = audio
        #         self.file_type = 'audio'
        if file.filename != '' and file.filename is not None:
            upload_time = datetime.datetime.now()
            now = upload_time.strftime('%Y%m%d%H%M%S')
            (folder, extension) = os.path.splitext(file.filename)
            filename = 'X_origin_' + str(now) + '_' + 'X' + '_VX_' + folder + extension
            fname = self.sets.save(storage=file, name=filename)
            url = self.sets.url(fname)
            return dict(filename=fname)
