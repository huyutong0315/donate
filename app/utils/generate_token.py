from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

# 传入字典类型data,生成一个token，默认有效期为10分钟
from app.libs.error_code import AuthFailed


def generate_token(data, expiration=600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps(data).decode('utf-8')


# 解析一个token，以字典方式进行返回
def decode_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # 序列化器 解密token
        data = s.loads(token)
    except BadSignature:
        # 如果解密失败，说明token不合法
        raise AuthFailed(msg='token is invalid',
                         error_code=10031)
    except SignatureExpired:
        # 签名过期
        raise AuthFailed(msg='token is expired',
                         error_code=10032)
    return data
