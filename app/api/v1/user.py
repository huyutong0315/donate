from flask import request, g
from sqlalchemy import or_

from app.api import photo
from app.libs.error import Success
from app.libs.error_code import LoginError
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.donar import Donar
from app.models.event import Event
from app.models.user import User
from app.models.wish import Wish
from app.utils.file import File
from app.validators.forms import RegisterForm, EmailLoginForm, NameLoginForm, PasswordForm, ChangePasswordForm
#describe   :   根据用户的用户名密码，进行用户注册
api = Redprint('user')
@api.route('/register',methods=['POST'])
def register():
    form = RegisterForm().validate_for_api()
    User.register(form.data)
    return Success(msg='注册成功')
#describe   :   登录时，对前端传回的token进行解析
@api.route('/token', methods=['POST'])
def token():
    if EmailLoginForm().validate_for_bool() or NameLoginForm().validate_for_bool():
        form = PasswordForm().validate_for_api()
        return Success(data=(User.account_verify(request.get_json(force=True))), msg='用户登录成功！')
        # return (User.account_verify(request.get_json(force=True)))
    else:
        return LoginError(msg='用户名不符合格式！',error_code=1016)
#describe   :   对用户的用户名进行修改，当用户名没有冲突时候修改成功
@api.route('/nickname', methods=['PUT'])
@auth.login_required
def update_nickname():
    data = request.get_json(force=True)
    uid = g.user.uid
    user = User.query.get_or_404(uid)
    user.update(data)
    return Success(data=user.id,msg='昵称更改成功！')
#describe   :   对用户的密码进行修改，当密码复合密码格式时，修改成功
@api.route('/password', methods=['PUT'])
@auth.login_required
def update_password():
    form = ChangePasswordForm().validate_for_api()
    uid = g.user.uid
    user = User.query.get_or_404(uid)
    user.update_password(form.data)
    return Success(msg='密码更改成功！')
#describe   :   查看自己的所有的心愿（所有状态）
@api.route('/my_wish',methods=['POST'])
@auth.login_required()
def my_wish():
    uid = g.user.uid
    wishes=Wish.query.filter_by(uid=uid).all()
    return Success(data=wishes,msg='获取自己的愿望成功')
#describe   :   查看自己的所有的捐赠（所有状态）
@api.route('/my_donar',methods=['POST'])
@auth.login_required()
def my_donar():
    uid = g.user.uid
    donars=Donar.query.filter_by(uid=uid).all()
    list=[]
    for donar in donars:
        pic_list=[]
        for value in donar.pic.values():
            pic_list.append(File(photo).get_file_url(value))
        item=dict(id=donar.id,content=donar.content,pic=pic_list,type=donar.type,status=donar.status)
        list.append(item)
    return Success(data=list,msg='获取自己的愿望成功')
#describe   :   查看自己的所有的事件（所有状态）
@api.route('/my_event',methods=['POST'])
@auth.login_required()
def my_event():
    uid = g.user.uid
    events=Event.query.filter(or_(Event.wish_user_id==uid,Event.donar_user_id==uid)).all()
    list=[]
    for event in events:
        item=dict(id=event.id,status=event.status,content=event.content,wish_id=event.wish_id,donar_id=event.donar_id,wish_user_id=event.wish_user_id,donar_user_id=event.donar_user_id,Initiator_id=event.Initiator_id)
        list.append(item)
    return Success(data=list,msg='获取事件成功')
#describe   :   查看心愿池（所有不是自己发布的心愿）
@api.route('/wish_pool',methods=['POST'])
@auth.login_required()
def wish_pool():
    uid=g.user.uid
    wishes=Wish.query.filter(Wish.uid!=uid,Wish.status==0).all()
    list=[]
    for wish in wishes:
        user =User.query.filter_by(id = wish.uid).first_or_404()
        item=dict(id=wish.id,content=wish.content,type=wish.type,role = user.role)
        list.append(item)
    return Success(data=list,msg='查看愿望池')
#describe   :   查看捐赠池（所有不是自己发布的捐赠）
@api.route('/donar_pool',methods=['POST'])
@auth.login_required()
def donar_pool():
    uid=g.user.uid
    donars=Donar.query.filter(Donar.uid!=uid,Donar.status==0).all()
    list=[]
    for donar in donars:
        item=dict(id=donar.id,content=donar.content,type=donar.type)
        list.append(item)
    return Success(data=list,msg='查看愿望池')
#describe   :   查看另一个用户的用户名，单位，email，手机号
@api.route('/another_user',methods=['POST'])
@auth.login_required()
def another_user():
    data=request.get_json()
    another_user_id=data['another_user_id']
    user=User.query.filter_by(id=another_user_id).first_or_404()
    data=dict(nickname=user.nickname,unit=user.unit,email=user.email,phone=user.phone)
    return Success(data=data,msg='获取用户信息')
#describe   :   查看个人的所有信息（用户名，单位，email，手机号，位置）
@api.route('/my_info',methods=['POST'])
@auth.login_required()
def my_info():
    uid=g.user.uid
    user=User.query.filter_by(id=uid).first_or_404()
    data = dict(nickname=user.nickname, unit=user.unit, email=user.email, phone=user.phone,location=user.location,integral = user.integral)
    return Success(data=data,msg='查看用户自己信息成功')