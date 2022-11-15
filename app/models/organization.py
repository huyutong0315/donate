from app.models import json2db
from app.models.base import Base
from sqlalchemy import Column,Integer,String,JSON
from sqlalchemy.ext.mutable import MutableDict
class Organization(Base):
    __tablename__ = 'organization'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),index=True)
    location = Column(String(255))
    describe = Column(String(255))
    pictures = Column(MutableDict.as_mutable(JSON))
    def update(self,data):
        organization = json2db(data, Organization)
        return dict(id = organization.id,location = organization.location,describe = organization.describe,pictures = organization.pictures)