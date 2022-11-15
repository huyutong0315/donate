import json

from flask import current_app
from authlib.jose import jwt

# 传入字典类型data,生成一个token，默认有效期为10分钟
from itsdangerous import BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed


def generate_token2(data, expiration=600):
    header = {'alg': 'HS512'}
    data['exp'] = expiration
    payload = data
    secret = current_app.config['SECRET_KEY']
    token = jwt.encode(header, payload, secret)
    s = token.decode('utf-8')
    return s


# 解析一个token，以字典方式进行返回
def decode_token2(token):
    try:
        # 序列化器 解密token
        data = jwt.decode(token,current_app.config['SECRET_KEY'])
    except BadSignature:
        # 如果解密失败，说明token不合法
        raise AuthFailed(msg='token is invalid',
                         error_code=10031)
    except SignatureExpired:
        # 签名过期
        raise AuthFailed(msg='token is expired',
                         error_code=10032)
    return data
