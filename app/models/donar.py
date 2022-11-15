from sqlalchemy import Column, Integer, Text, JSON, String

from app.models import json2db
from app.models.base import Base
from app.models.picture import Picture

#捐赠类
class Donar(Base):
    __tablename__ = 'donar'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid=Column(Integer,index=True)
    content=Column(Text)
    pic=Column(JSON)
    type = Column(String(255), index=True)
    status = Column(Integer, index=True)
    #add方法是来增加新的捐赠的
    def add(self,uid,pictures,content,type):
        pic_dict={}
        i=0
        for picture in pictures:
            pic_id=Picture().add(picture)
            pic_dict[i]=pic_id
            i=i+1
        data=dict(uid=uid,content=content,pic=pic_dict,type=type,status=0)
        json2db(data,Donar)

