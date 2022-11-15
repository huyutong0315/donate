from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import ServerError

class JSONEncoder(_JSONEncoder):
    # default其实是递归调用的，不能序列化的都将调用default
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # 如果对象里面，有属性是时间对象，另外处理
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')

        raise ServerError(msg="jsonify模型对象失败")  # 具体的错误信息反馈到客户端,也没用，返回一个统一的


# 使得生成app的Flask方法 是我们覆盖json_encoder的flask
class Flask(_Flask):
    json_encoder = JSONEncoder
