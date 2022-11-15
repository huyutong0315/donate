from flask import request, g

from app.api import photo
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import db
from app.models.donar import Donar
from app.models.event import Event
from app.models.user import User
from app.models.wish import Wish
from app.utils.file import File

api = Redprint('/donar')
# parameter:
##content   :   对自己的捐赠的描述
##type  : 捐赠的种类（文具，书籍等）
#return :   字符串 "发布捐赠成功"
#describe   :   此接口为发布的捐赠
@api.route('/publish',methods=['POST'])
@auth.login_required
def publish():
    uid = g.user.uid
    pictures=request.files.getlist('pictures')
    content=request.form['content']
    type=request.form['type']
    Donar().add(uid,pictures,content,type)
    return Success(msg='发布捐赠成功')
# parameter:
##donar_id   :   自己捐赠的id
##another_id  : 另一个人的用户id（用来找到用心愿人的信息）
##wish_id   ： 另外来匹配的心愿
##content   :   对自己的捐赠的描述
#return :   字符串 '发起匹配'
#describe   :   这个接口为用自己的捐赠去申请匹配另外一个人的心愿，心愿和捐赠的状态改为1
@api.route('/match',methods=['POST'])
@auth.login_required
def match():
    data=request.get_json(force=True)
    uid=g.user.uid
    donar_id=data['donar_id']
    another_id=data['another_id']
    wish_id=data['wish_id']
    content=data['content']

    donar=Donar.query.filter_by(id=donar_id).first_or_404()
    wish = Wish.query.filter_by(id=wish_id).first_or_404()
    with db.auto_commit():
        donar.status=1
        wish.status=1
    data=dict(donar_user_id=uid,donar_id=donar_id, wish_user_id=another_id,wish_id=wish_id,content=content,Initiator_id=uid,status=0)
    Event().add(data)
    return Success(msg='发起匹配')
# parameter:
##event_id  :   传入事件的id
##accept    :   传入对方是否同意这个请求
#describe   :   如果事件被接受，将事件，心愿，捐赠的状态改为1，如果事件被拒绝，将事件的状态改为3，心愿和捐赠的状态改为0
#return :   如果被接受，返回字符串'匹配成功'，如果被拒绝，返回字符串'拒绝'
@api.route('/accept',methods=['POST'])
@auth.login_required
def accept():
    data=request.get_json(force=True)
    event_id=data['event_id']
    accept=data['accept']#0拒绝，1同意
    event=Event.query.filter_by(id=event_id).first_or_404()
    wish=Wish.query.filter_by(id=event.wish_id).first_or_404()
    donar=Donar.query.filter_by(id=event.donar_id).first_or_404()
    if accept:
        with db.auto_commit():
            event.status = 1
        with db.auto_commit():
            wish.status = 1
        with db.auto_commit():
            donar.status = 1
        return Success(msg='匹配成功')
    else:
        with db.auto_commit():
            event.status = 3
        with db.auto_commit():
            wish.status = 0
        with db.auto_commit():
            donar.status = 0
        return Success(msg='拒绝')
# parameter:
##donar_id  ：   捐赠的id
#return :   content(捐赠的内容） pic（没有用到）    type（捐赠的类型）    name(捐赠者的名字）     uid(捐赠者的id)
@api.route('/detail',methods=['POST'])
@auth.login_required()
def detail():
    data = request.get_json(force=True)
    donar_id=data['donar_id']
    donar=Donar.query.filter_by(id=donar_id).first_or_404()
    pic_list = []
    for value in donar.pic.values():
        pic_list.append(File(photo).get_file_url(value))
    user=User.query.filter_by(id=donar.uid).first_or_404()
    data=dict(content=donar.content,pic=pic_list,type=donar.type,name=user.nickname,unit=user.unit,uid=user.id)
    return Success(data=data,msg='返回捐赠细节')
