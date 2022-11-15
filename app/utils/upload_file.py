import os

from flask import current_app

from app.api import audio,photo
from app.utils.folder import create_folder


def upload_file(file):
    sets = None
    # 这里一个bug， postman传过来的中文文件最后加了个"
    if file.filename.endswith('\"'):
        file.filename = file.filename[:-1]
        print('delete \"')
    (folder, extension) = os.path.splitext(file.filename)
    extension = extension[1:]
    if extension in ('jpg','png','jpeg','JPG','PNG','JPEG'):
        sets = photo
    elif extension in ('wav', "mp3'"):
        sets = audio
    if file.filename != '':
        fname = sets.save(storage=file, name=file.filename)
        url = sets.url(fname)
    return dict(filename=fname, url=url, file_type='photo' if sets == photo else 'audio')


def get_file_url(fname):
    (folder, extension) = os.path.splitext(fname)
    extension = extension[1:]
    if extension in ('jpg','png','jpeg','JPG','PNG','JPEG'):
        sets = photo
    elif extension in ('wav','mp3'):
        sets = audio
    return sets.url(fname)

def get_file_path(fname):
    if fname is not None and fname != '':
        (folder, extension) = os.path.splitext(fname)
        extension = extension[1:]
        if extension in ('jpg','png','jpeg','JPG','PNG','JPEG'):
            sets = photo
        elif extension in ('mp3',):
            sets = audio
        return sets.path(fname)

def delete_file(path):
    if path is not None and path != '':
        if os.path.exists(path):
            os.remove(path)