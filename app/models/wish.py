from sqlalchemy import Column, Integer, Text, JSON, String, orm

from app.models import json2db
from app.models.base import Base

#心愿类
class Wish(Base):
    __tablename__ = 'wish'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, index=True)
    content = Column(Text)
    type=Column(String(255),index=True)
    status = Column(Integer, index=True)

    @orm.reconstructor
    def __init__(self):
        self.fields=['id','content','type','status']
    def add(self,uid,content,type):
        data=dict(uid=uid,content=content,type=type,status=0)
        json2db(data,Wish)
