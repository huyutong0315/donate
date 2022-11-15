from app.api import photo
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.picture import Picture
from flask import request

from app.utils.file import File

api = Redprint('picture')

@api.route('/add_picture',methods=['POST'])
@auth.login_required
def add_picture():
    data = Picture().add(request.files.get('picture'))
    return Success(data = data if data else {},msg = '成功上传照片')

@api.route('/get_picture',methods=['POST'])
@auth.login_required
def grt_picture():
    data = request.get_json(force=True)
    picture = Picture.query.filter_by(id = data['id']).first_or_404()
    return Success(data=dict(url = File(photo).get_file_url(picture.filename)),msg='照片详细信息')