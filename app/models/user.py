from flask import current_app
from sqlalchemy import Column, Integer, String, SmallInteger, orm, or_, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import RoleTypeEnum
from app.libs.error_code import NotFound, AuthFailed, LoginError, NameRepeated
from app.libs.token_auth import update_visit_time
from app.models import json2db_add, json2db
from app.models.base import Base, db
from app.utils.generate_token import generate_token
from app.utils.generate_token2 import generate_token2
#用户类，主要是记录了用户的一些基本信息
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    #用户的id主键，用来区别不同的用户
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname=Column(String(255),index=True)
    location=Column(String(255),index=True)
    unit=Column(String(255),index=True)
    email = Column(String(40), unique=True, nullable=False, index=True)
    phone=Column(String(255),index=True,nullable=False)
    _password = Column('password', String(400))
    #来标记用户的身份是否为爱心妈妈,0是普通用户，1是爱心妈妈
    role = Column(Integer,default=0,index = True)
    #用户的积分
    integral =Column(Integer,default=0,index = True)
    #用户登录的访问日期（自动更新）
    visit_date = Column(DateTime, index=True)
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'nickname']

    @property
    def password(self):
        return self._password
    #对用户传过来的明文密码进行一次哈希加密
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
    #未用
    @property
    def role_str(self):
        return RoleTypeEnum.step_str(RoleTypeEnum(self.role))

    # @property
    # def auth_str(self):
    #     return ScopeTypeEnum.step_str(ScopeTypeEnum(self.auth))

    # 类下面创建类本身对象用静态方法或者类方法
    #用户注册
    @staticmethod
    def register(data):
        print(data)
        json2db(data, User)

    # @staticmethod
    # def activate(data):
    #     with db.auto_commit():
    #         user = User.query.filter_by(nickname=data.get('nickname')).first_or_404()
    #         user.auth = 3
    #对传入的token进行解码，看用户是否存在
    @staticmethod
    def account_verify(data):
        user = User.query.filter(or_(User.email == data.get('account'), User.nickname == data.get('account'))).first()
        if not user:
            raise LoginError(error_code=1014, msg='用户不存在')
        return user.check_pwd(data.get('password'))
    #对解码后的账户名密码进行验证，看密码是否正确
    def check_pwd(self, password):
        if not check_password_hash(self.password, password):
            raise LoginError(error_code=1017, msg='用户密码错误')
        data = {'uid': self.id, "nickname": self.nickname, 'email': self.email}
        res = {'token': generate_token2(data, expiration=current_app.config['LOGIN_TOKEN_EXPIRATION']),
               "nickname": self.nickname,
               "uid":self.id,
               "role":self.role,
               "integral":self.integral}
        update_visit_time(self.id)
        return res

    #更新用户的信息
    def update(self, data):
        user_temp = User.query.filter(or_(User.nickname==data['nickname'],User.email==data["email"],User.phone==data["phone"])).first()
        with db.auto_commit():
            # 数据库中没有名字记录，则可以进行更新
            if not user_temp:
                self.nickname = data["nickname"]
                self.email=data["email"]
                self.phone=data["phone"]
                self.unit=data["unit"]
                self.location=data["location"]
            # 存在，且是别的id，则报重复错
            if user_temp and user_temp.id != self.id:
                raise NameRepeated()

    #更新用户的密码
    def update_password(self, data):
        if not check_password_hash(self.password, data['oldpassword']):
            raise LoginError(error_code=1017, msg='用户密码错误')
        else:
            with db.auto_commit():
                self.password = data['newpassword']
    #管理员对密码进行更改（未用）
    def update_password_by_admin(self, data):
        with db.auto_commit():
            self.password = data['newpassword']
    # #新增用户
    # def add(self, nickname, password):
    #     data = dict(nickname=nickname, _password=generate_password_hash(password),
    #                 email=nickname + '@' + 'teacher' + '.com', role=2)
    #     json2db(data, User)
