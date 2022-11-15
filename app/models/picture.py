from sqlalchemy import Column, Integer, String

from app.api import photo
from app.models import json2db_add
from app.utils.file import File
from app.models.base import Base, db


class Picture(Base):
    __tablename__ = 'picure'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename=Column(String(255),index=True)
    def add(self,picture_file):
        file = File(photo)
        data = file.upload_file(picture_file)
        pic=json2db_add(data,Picture)
        return dict(id = pic.id,filename = pic.filename,url = file.get_file_url(data['filename']))