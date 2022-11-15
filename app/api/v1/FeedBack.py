from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.feedback import FeedBack
api = Redprint('feedback')
@api.route("/add",methods=['POST'])
@auth.login_required
def add():
    data = request.get_json(force=True)
    feedback = FeedBack().update(data)
    return Success(data=feedback ,msg = '上传反馈成功')

@api.route("/list",methods=['POST'])
@auth.login_required
def list():
    fds = FeedBack.query.filter_by().all()
    item = []
    for fd in fds:
        item.append(dict(id = fd.id,describe=fd.describe,name = fd.name,pictures=fd.pictures if fd.pictures else {}))
    return Success(data = item ,msg = '反馈列表')

@api.route("/update",methods=['POST'])
@auth.login_required
def update():
    data = request.get_json(force=True)
    feedback = FeedBack.query.filter_by(id = data['id']).first_or_404()
    feedback.update(data)
    return Success(data=dict(id= feedback.id,describe=feedback.describe,name = feedback.name,pictures=feedback.pictures if feedback.pictures else {}) ,msg = '上传反馈成功')