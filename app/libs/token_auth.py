from collections import namedtuple
from datetime import datetime,timedelta

from flask import g, request
from flask_httpauth import HTTPTokenAuth
from app.libs.error_code import Forbidden
from app.libs.scope import is_in_scope
from app.models import db
from app.utils.generate_token import decode_token
from app.utils.generate_token2 import decode_token2

auth = HTTPTokenAuth()

User = namedtuple('User', ['uid', 'nickname', 'email'])


@auth.verify_token
def verify_token(token):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        update_visit_time(g.user.uid)
        return True


def verify_auth_token(token):
    data = decode_token2(token)
    # allow = is_in_scope(data.get('scope'), request.endpoint)
    # if not allow:
    #     raise Forbidden()
    return User(data.get('uid'), data.get('nickname'), data.get('email'))


def update_visit_time(uid):
    from app.models.user import User as User_Q
    user = User_Q.query.get_or_404(uid)
    now = datetime.now()
    with db.auto_commit():
        user.visit_date = now