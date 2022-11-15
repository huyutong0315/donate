import os

TOKEN_EXPIRATION = 30 * 24 * 3600
LOGIN_TOKEN_EXPIRATION = 30 * 24 * 3600
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_CONTENT_LENGTH = 100 * 1024 * 1024
UPLOADS_AUTOSERVE = True
UPLOADED_PHOTO_DEST = (os.getcwd() + '/app/static/uploads/photos').replace('\\', '/')
UPLOADED_AUDIO_DEST = (os.getcwd() + '/app/static/uploads/audios').replace('\\', '/')
UPLOADED_DOCUMENT_DEST = (os.getcwd() + '/app/static/uploads/documents').replace('\\', '/')

COMPRESS_ALGORITHM = 'gzip'
COMPRESS_LEVEL = 6