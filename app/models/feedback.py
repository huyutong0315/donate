from app.models import json2db
from app.models.base import Base
from sqlalchemy import Column,Integer,String,JSON
from sqlalchemy.ext.mutable import MutableDict
class FeedBack(Base):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    describe = Column(String(255))
    name = Column(String(255))
    pictures = Column(MutableDict.as_mutable(JSON))
    def update(self,data):
        feedback=json2db(data,FeedBack)
        return dict(id = feedback.id ,describe= feedback.describe,pictures = feedback.pictures,name = feedback.name)