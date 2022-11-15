from flask import request

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.organization import Organization
api = Redprint('Organization')


@api.route("/detail",methods=['POST'])
@auth.login_required
def detail():
    organization = Organization.query.filter_by(id = 1).first_or_404()

    return Success(data = dict(id = organization.id,name=organization.name,location = organization.location,describe = organization.describe,pictures = organization.pictures if organization.pictures else {}),msg = '查看爱心妈妈组织详细信息')

@api.route("/update",methods=['POST'])
@auth.login_required
def update():
    data = request.get_json(force=True)
    organization = Organization.query.filter_by(id=1).first_or_404()
    data['id']=1
    organization.update(data)
    return Success(data = dict(id = organization.id,location = organization.location,describe = organization.describe,pictures = organization.pictures),msg = '修改爱心妈妈组织信息成功')

