from sqlalchemy import Column, Integer, Text

from app.models import json2db
from app.models.base import Base

#事件类，用来记录每一次的事件
class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'extend_existing': True}
    #id，用来区分不同的事件
    id = Column(Integer, primary_key=True, autoincrement=True)
    wish_user_id = Column(Integer, index=True)
    wish_id=Column(Integer,index=True)
    donar_user_id = Column(Integer, index=True)
    donar_id=Column(Integer,index=True)
    status=Column(Integer,index=True)
    Initiator_id=Column(Integer,index=True)
    content=Column(Text)
    def add(self,data):
        json2db(data,Event)